from flask import Flask, render_template, request
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

app = Flask(__name__)

ARCHIVO_ONTOLOGIA = Path("ontologia/reposteria.owx")


def nombre_xml(elemento):
    return elemento.tag.split("}", 1)[-1]


def limpiar_iri(valor):
    if not valor:
        return ""
    return valor.replace("#", "").split("/")[-1]


def obtener_iri(elemento):
    return limpiar_iri(
        elemento.attrib.get("IRI")
        or elemento.attrib.get("abbreviatedIRI")
        or ""
    )


def cargar_ontologia():
    arbol = ET.parse(ARCHIVO_ONTOLOGIA)
    raiz = arbol.getroot()

    datos = {
        "clases": set(),
        "propiedades_objeto": set(),
        "propiedades_datos": set(),
        "individuos": set(),
        "superclases": defaultdict(set),
        "clases_individuo": defaultdict(set),
        "relaciones_salida": defaultdict(lambda: defaultdict(list)),
        "relaciones_entrada": defaultdict(lambda: defaultdict(list)),
        "atributos": defaultdict(lambda: defaultdict(list)),
    }

    for declaracion in raiz:
        if nombre_xml(declaracion) != "Declaration" or len(declaracion) == 0:
            continue

        entidad = declaracion[0]
        tipo = nombre_xml(entidad)
        iri = obtener_iri(entidad)

        if tipo == "Class":
            datos["clases"].add(iri)
        elif tipo == "ObjectProperty":
            datos["propiedades_objeto"].add(iri)
        elif tipo == "DataProperty":
            datos["propiedades_datos"].add(iri)
        elif tipo == "NamedIndividual":
            datos["individuos"].add(iri)

    for axioma in raiz:
        tipo_axioma = nombre_xml(axioma)
        hijos = list(axioma)

        if tipo_axioma == "SubClassOf" and len(hijos) >= 2:
            subclase = obtener_iri(hijos[0])
            superclase = obtener_iri(hijos[1])

            if subclase and superclase:
                datos["superclases"][subclase].add(superclase)

        elif tipo_axioma == "ClassAssertion" and len(hijos) >= 2:
            clase = obtener_iri(hijos[0])
            individuo = obtener_iri(hijos[1])

            if individuo and clase:
                datos["clases_individuo"][individuo].add(clase)

        elif tipo_axioma == "ObjectPropertyAssertion" and len(hijos) >= 3:
            propiedad = obtener_iri(hijos[0])
            sujeto = obtener_iri(hijos[1])
            objeto = obtener_iri(hijos[2])

            if sujeto and propiedad and objeto:
                datos["relaciones_salida"][sujeto][propiedad].append(objeto)
                datos["relaciones_entrada"][objeto][propiedad].append(sujeto)

        elif tipo_axioma == "DataPropertyAssertion" and len(hijos) >= 3:
            propiedad = obtener_iri(hijos[0])
            sujeto = obtener_iri(hijos[1])
            valor = "".join(hijos[2].itertext()).strip()

            if sujeto and propiedad and valor:
                datos["atributos"][sujeto][propiedad].append(valor)

    return datos


ONTOLOGIA = cargar_ontologia()


def obtener_superclases(clase, visitadas=None):
    if visitadas is None:
        visitadas = set()

    for superior in ONTOLOGIA["superclases"].get(clase, set()):
        if superior not in visitadas:
            visitadas.add(superior)
            obtener_superclases(superior, visitadas)

    return sorted(visitadas)


def texto_busqueda_individuo(individuo):
    partes = [individuo]

    clases = ONTOLOGIA["clases_individuo"].get(individuo, [])
    partes.extend(clases)

    for clase in clases:
        partes.extend(obtener_superclases(clase))

    for propiedad, objetos in ONTOLOGIA["relaciones_salida"].get(individuo, {}).items():
        partes.append(propiedad)
        partes.extend(objetos)

    for propiedad, valores in ONTOLOGIA["atributos"].get(individuo, {}).items():
        partes.append(propiedad)
        partes.extend(valores)

    return " ".join(partes).lower()


def buscar(termino):
    termino = termino.strip().lower()
    resultados = []

    if not termino:
        return resultados

    for individuo in sorted(ONTOLOGIA["individuos"]):
        if termino in texto_busqueda_individuo(individuo):
            clases = sorted(ONTOLOGIA["clases_individuo"].get(individuo, []))

            superclases = sorted({
                superior
                for clase in clases
                for superior in obtener_superclases(clase)
            })

            resultados.append({
                "nombre": individuo,
                "tipo": "Individuo",
                "clases": clases,
                "superclases": superclases,
                "atributos": dict(ONTOLOGIA["atributos"].get(individuo, {})),
                "relaciones": dict(ONTOLOGIA["relaciones_salida"].get(individuo, {})),
                "usado_en": dict(ONTOLOGIA["relaciones_entrada"].get(individuo, {})),
            })

    for clase in sorted(ONTOLOGIA["clases"]):
        if termino in clase.lower():
            resultados.append({
                "nombre": clase,
                "tipo": "Clase",
                "clases": [],
                "superclases": obtener_superclases(clase),
                "atributos": {},
                "relaciones": {},
                "usado_en": {},
            })

    return resultados


@app.route("/", methods=["GET", "POST"])
def inicio():
    termino = ""

    if request.method == "POST":
        termino = request.form.get("termino", "")

    resultados = buscar(termino)

    resumen = {
        "clases": len(ONTOLOGIA["clases"]),
        "propiedades_objeto": len(ONTOLOGIA["propiedades_objeto"]),
        "propiedades_datos": len(ONTOLOGIA["propiedades_datos"]),
        "individuos": len(ONTOLOGIA["individuos"]),
    }

    return render_template(
        "index.html",
        termino=termino,
        resultados=resultados,
        resumen=resumen
    )


if __name__ == "__main__":
    app.run(debug=True)