from flask import Flask, jsonify, request
from pathlib import Path
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import defaultdict
from time import perf_counter

from services.dbpedia import consultar_dbpedia

app = Flask(__name__, static_folder=None, template_folder=None)

ARCHIVO_ONTOLOGIA = Path(__file__).resolve().parent / "ontologia" / "reposteria.owx"

PALABRAS_VACIAS = {
    "de", "del", "la", "las", "el", "los",
    "un", "una", "unos", "unas", "y", "con", "para"
}


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


def separar_camel_case(texto):
    texto = re.sub(r"([a-záéíóúñ])([A-ZÁÉÍÓÚÑ])", r"\1 \2", texto)
    texto = re.sub(r"([A-ZÁÉÍÓÚÑ]+)([A-ZÁÉÍÓÚÑ][a-záéíóúñ])", r"\1 \2", texto)
    return texto


def quitar_tildes(texto):
    texto_normalizado = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter for caracter in texto_normalizado
        if unicodedata.category(caracter) != "Mn"
    )


def normalizar_texto(texto):
    texto = separar_camel_case(str(texto))
    texto = quitar_tildes(texto)
    texto = texto.lower()
    texto = re.sub(r"[_\-.;,:/()\[\]{}]+", " ", texto)
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def variantes_token(token):
    variantes = {token}

    if len(token) > 4 and token.endswith("s"):
        variantes.add(token[:-1])

    if len(token) > 5 and token.endswith("es"):
        variantes.add(token[:-2])

    if len(token) > 5 and token.endswith("ces"):
        variantes.add(token[:-3] + "z")

    return {variante for variante in variantes if len(variante) >= 2}


def tokenizar_busqueda(texto):
    tokens = []

    for token in normalizar_texto(texto).split():
        if token in PALABRAS_VACIAS:
            continue

        for variante in variantes_token(token):
            if variante not in PALABRAS_VACIAS and variante not in tokens:
                tokens.append(variante)

    return tokens


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

    return " ".join(partes)


def construir_indice_busqueda():
    indice = []

    for individuo in sorted(ONTOLOGIA["individuos"]):
        texto_original = texto_busqueda_individuo(individuo)
        texto_normalizado = normalizar_texto(texto_original)
        tokens = set(tokenizar_busqueda(texto_original))

        indice.append({
            "nombre": individuo,
            "tipo": "Individuo",
            "texto": texto_normalizado,
            "compacto": texto_normalizado.replace(" ", ""),
            "tokens": tokens,
        })

    for clase in sorted(ONTOLOGIA["clases"]):
        texto_original = " ".join([clase, *obtener_superclases(clase)])
        texto_normalizado = normalizar_texto(texto_original)
        tokens = set(tokenizar_busqueda(texto_original))

        indice.append({
            "nombre": clase,
            "tipo": "Clase",
            "texto": texto_normalizado,
            "compacto": texto_normalizado.replace(" ", ""),
            "tokens": tokens,
        })

    return indice


INDICE_BUSQUEDA = construir_indice_busqueda()


def resultado_individuo(individuo):
    clases = sorted(ONTOLOGIA["clases_individuo"].get(individuo, []))

    superclases = sorted({
        superior
        for clase in clases
        for superior in obtener_superclases(clase)
    })

    return {
        "nombre": individuo,
        "tipo": "Individuo",
        "clases": clases,
        "superclases": superclases,
        "atributos": dict(ONTOLOGIA["atributos"].get(individuo, {})),
        "relaciones": dict(ONTOLOGIA["relaciones_salida"].get(individuo, {})),
        "usado_en": dict(ONTOLOGIA["relaciones_entrada"].get(individuo, {})),
    }


def resultado_clase(clase):
    return {
        "nombre": clase,
        "tipo": "Clase",
        "clases": [],
        "superclases": obtener_superclases(clase),
        "atributos": {},
        "relaciones": {},
        "usado_en": {},
    }


def calcular_puntaje(item, consulta_normalizada, consulta_compacta, tokens_base):
    frase_completa = consulta_normalizada and consulta_normalizada in item["texto"]
    nombre_unido = consulta_compacta and consulta_compacta in item["compacto"]

    tokens_encontrados = 0
    coincide_todo = False

    if tokens_base:
        resultados_tokens = []

        for token in tokens_base:
            coincide_token = any(
                variante in item["tokens"]
                or variante in item["texto"]
                or variante in item["compacto"]
                for variante in variantes_token(token)
            )
            resultados_tokens.append(coincide_token)

        tokens_encontrados = sum(1 for coincide in resultados_tokens if coincide)
        coincide_todo = all(resultados_tokens)

    if len(tokens_base) >= 2 and not (frase_completa or nombre_unido or coincide_todo):
        return 0

    puntaje = 0

    if frase_completa:
        puntaje += 100

    if nombre_unido:
        puntaje += 90

    if coincide_todo:
        puntaje += 60 + tokens_encontrados * 10
    else:
        puntaje += tokens_encontrados * 10

    return puntaje


def buscar(termino):
    consulta_normalizada = normalizar_texto(termino)
    consulta_compacta = consulta_normalizada.replace(" ", "")

    tokens_base = [
        token for token in consulta_normalizada.split()
        if token not in PALABRAS_VACIAS
    ]

    if not consulta_normalizada:
        return []

    coincidencias = []

    for item in INDICE_BUSQUEDA:
        puntaje = calcular_puntaje(
            item,
            consulta_normalizada,
            consulta_compacta,
            tokens_base,
        )

        if puntaje > 0:
            coincidencias.append((puntaje, item))

    if not coincidencias and len(tokens_base) >= 2:
        for item in INDICE_BUSQUEDA:
            tokens_encontrados = 0

            for token in tokens_base:
                if any(
                    variante in item["tokens"]
                    or variante in item["texto"]
                    or variante in item["compacto"]
                    for variante in variantes_token(token)
                ):
                    tokens_encontrados += 1

            if tokens_encontrados > 0:
                coincidencias.append((tokens_encontrados * 10, item))

    coincidencias.sort(key=lambda dato: (-dato[0], dato[1]["tipo"], dato[1]["nombre"]))

    resultados = []
    nombres_agregados = set()

    for _, item in coincidencias:
        nombre = item["nombre"]

        if nombre in nombres_agregados:
            continue

        nombres_agregados.add(nombre)

        if item["tipo"] == "Individuo":
            resultados.append(resultado_individuo(nombre))
        else:
            resultados.append(resultado_clase(nombre))

    return resultados


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
    inicio = perf_counter()

    termino = request.args.get("termino", "")
    usar_dbpedia = request.args.get("dbpedia", "1") != "0"

    resultados_locales = buscar(termino)
    resultados_dbpedia = consultar_dbpedia(termino) if usar_dbpedia else []

    tiempo_ms = round((perf_counter() - inicio) * 1000, 2)

    return jsonify({
        "resultados": resultados_locales,
        "dbpedia": resultados_dbpedia,
        "total": len(resultados_locales) + len(resultados_dbpedia),
        "tiempo_ms": tiempo_ms,
        "fuentes": {
            "local": len(resultados_locales),
            "dbpedia": len(resultados_dbpedia),
        },
    })


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)