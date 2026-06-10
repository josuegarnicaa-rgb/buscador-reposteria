from flask import Flask, jsonify, request
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

from services.dbpedia import consultar_dbpedia
from services.dbpedia_local import buscar_dbpedia_local
from services.i18n import (
    normalizar_idioma,
    normalizar_texto,
    traducir_identificador,
    traducir_lista,
    traducir_mapa,
    traducir_origen,
    traducir_al_esp,
)
from utils.text_conec import quitar_conectores

app = Flask(__name__, static_folder=None, template_folder=None)

ARCHIVO_ONTOLOGIA = Path(__file__).resolve().parent / "ontologia" / "reposteria.owx"


@app.after_request
def agregar_cors(respuesta):
    respuesta.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    respuesta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    respuesta.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return respuesta


def nombre_xml(elemento):
    return elemento.tag.split("}", 1)[-1]


def limpiar_iri(valor):
    if not valor:
        return ""
    return valor.replace("#", "").split("/")[-1]


def obtener_iri(elemento):
    return limpiar_iri(
        elemento.attrib.get("IRI") or elemento.attrib.get("abbreviatedIRI") or ""
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


def texto_busqueda_individuo(individuo, idioma):
    partes = [individuo, traducir_identificador(individuo, idioma)]

    clases = ONTOLOGIA["clases_individuo"].get(individuo, [])
    partes.extend(clases)
    partes.extend(traducir_lista(clases, idioma))

    for clase in clases:
        superclases = obtener_superclases(clase)
        partes.extend(superclases)
        partes.extend(traducir_lista(superclases, idioma))

    for propiedad, objetos in ONTOLOGIA["relaciones_salida"].get(individuo, {}).items():
        partes.append(propiedad)
        partes.extend(objetos)
        partes.append(traducir_identificador(propiedad, idioma))
        partes.extend(traducir_lista(objetos, idioma))

    for propiedad, valores in ONTOLOGIA["atributos"].get(individuo, {}).items():
        partes.append(propiedad)
        partes.extend(valores)
        partes.append(traducir_identificador(propiedad, idioma))
        partes.extend(traducir_lista(valores, idioma))

    return normalizar_texto(" ".join(partes))


def traducir_resultado(resultado, idioma):
    return {
        "id": resultado["nombre"],
        "nombre": traducir_identificador(resultado["nombre"], idioma),
        "tipo": traducir_al_esp(resultado["tipo"], idioma),
        "clases": traducir_lista(resultado["clases"], idioma),
        "superclases": traducir_lista(resultado["superclases"], idioma),
        "atributos": traducir_mapa(resultado["atributos"], idioma),
        "relaciones": traducir_mapa(resultado["relaciones"], idioma),
        "usado_en": traducir_mapa(resultado["usado_en"], idioma),
        "origen": traducir_origen("LOCAL", idioma),
    }


def buscar(termino, idioma="es"):
    idioma = normalizar_idioma(idioma)
    termino = normalizar_texto(termino)
    resultados = []

    if not termino:
        return resultados

    for individuo in sorted(ONTOLOGIA["individuos"]):
        if termino in texto_busqueda_individuo(individuo, idioma):
            clases = sorted(ONTOLOGIA["clases_individuo"].get(individuo, []))

            superclases = sorted(
                {
                    superior
                    for clase in clases
                    for superior in obtener_superclases(clase)
                }
            )

            resultados.append(
                {
                    "nombre": individuo,
                    "tipo": "Individuo",
                    "clases": clases,
                    "superclases": superclases,
                    "atributos": dict(ONTOLOGIA["atributos"].get(individuo, {})),
                    "relaciones": dict(
                        ONTOLOGIA["relaciones_salida"].get(individuo, {})
                    ),
                    "usado_en": dict(
                        ONTOLOGIA["relaciones_entrada"].get(individuo, {})
                    ),
                }
            )

    for clase in sorted(ONTOLOGIA["clases"]):
        nombre_traducido = traducir_identificador(clase, idioma)
        if termino in normalizar_texto(nombre_traducido) or termino in normalizar_texto(
            clase
        ):
            resultados.append(
                {
                    "nombre": clase,
                    "tipo": "Clase",
                    "clases": [],
                    "superclases": obtener_superclases(clase),
                    "atributos": {},
                    "relaciones": {},
                    "usado_en": {},
                }
            )

    return [traducir_resultado(resultado, idioma) for resultado in resultados]


def obtener_resumen():
    return {
        "clases": len(ONTOLOGIA["clases"]),
        "propiedades_objeto": len(ONTOLOGIA["propiedades_objeto"]),
        "propiedades_datos": len(ONTOLOGIA["propiedades_datos"]),
        "individuos": len(ONTOLOGIA["individuos"]),
    }


@app.get("/api/resumen")
def api_resumen():
    return jsonify(obtener_resumen())


@app.get("/api/buscar")
def api_buscar():
    termino_original = request.args.get("termino", "")
    idioma = normalizar_idioma(request.args.get("idioma", "es"))
    termino_en_esp = traducir_al_esp(termino_original, idioma)
    resultados_locales = buscar(quitar_conectores(termino_en_esp), idioma)
    resultados_dbpedia_remotos = consultar_dbpedia(termino_original, idioma)
    resultados_dbpedia_locales = buscar_dbpedia_local(termino_original, idioma)

    return jsonify(
        {
            "resultados": resultados_locales,
            "dbpedia": resultados_dbpedia_remotos + resultados_dbpedia_locales,
            "total": len(resultados_locales)
            + len(resultados_dbpedia_remotos)
            + len(resultados_dbpedia_locales),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
