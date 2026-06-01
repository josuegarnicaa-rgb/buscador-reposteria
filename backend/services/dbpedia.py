from functools import lru_cache
from pathlib import Path
import html
import json
import os
import re
import unicodedata
import requests

DBPEDIA_LOOKUP_ENDPOINT = "https://lookup.dbpedia.org/api/search"

BASE_DIR = Path(__file__).resolve().parents[1]
ARCHIVO_DBPEDIA_LOCAL = BASE_DIR / "data" / "dbpedia_reposteria.json"

PALABRAS_VACIAS = {
    "de", "del", "la", "las", "el", "los",
    "un", "una", "unos", "unas", "y", "con", "para"
}

PALABRAS_REPOSTERIA = {
    "torta", "tart", "cake", "pastel", "galleta", "galletas", "cookie", "cookies",
    "chocolate", "crema", "fresa", "frutilla", "vainilla", "postre", "dessert",
    "dulce", "bizcocho", "masa", "harina", "azucar", "azúcar", "mantequilla",
    "leche", "queso", "pan", "panaderia", "panadería", "reposteria", "repostería",
    "ingrediente", "receta", "pie", "brownie", "muffin", "cupcake", "flan",
    "gelatina", "merengue", "crepe", "waffle", "donut", "rosquilla"
}

PALABRAS_NO_REPOSTERIA = {
    "country", "place", "settlement", "town", "city", "populatedplace",
    "person", "politician", "football", "album", "song", "film",
    "river", "mountain", "company", "organisation", "organization"
}


def dbpedia_online_activado():
    valor = os.getenv("USE_DBPEDIA", "false").strip().lower()
    return valor in {"1", "true", "yes", "si", "sí"}


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


def quitar_html(texto):
    texto = str(texto or "")
    texto = re.sub(r"<[^>]+>", "", texto)
    return html.unescape(texto)


def normalizar_texto(texto):
    texto = quitar_html(texto)
    texto = separar_camel_case(str(texto))
    texto = quitar_tildes(texto)
    texto = texto.lower()
    texto = re.sub(r"[_\-.;,:/()\[\]{}]+", " ", texto)
    texto = re.sub(r"[^a-z0-9ñ\s]", " ", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto


def tokenizar(texto):
    return [
        token for token in normalizar_texto(texto).split()
        if token and token not in PALABRAS_VACIAS
    ]


@lru_cache(maxsize=1)
def cargar_dbpedia_local():
    if not ARCHIVO_DBPEDIA_LOCAL.exists():
        return []

    with ARCHIVO_DBPEDIA_LOCAL.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def consultar_dbpedia_offline(termino, limite=6):
    consulta = normalizar_texto(termino)
    consulta_compacta = consulta.replace(" ", "")
    tokens = tokenizar(termino)

    if not consulta:
        return []

    coincidencias = []

    for item in cargar_dbpedia_local():
        texto_item = " ".join([
            item.get("nombre", ""),
            item.get("abstract", ""),
            item.get("typeLabel", ""),
            " ".join(item.get("countries", [])),
            " ".join(item.get("ingredientes", [])),
        ])

        texto_normalizado = normalizar_texto(texto_item)
        texto_compacto = texto_normalizado.replace(" ", "")

        puntaje = 0

        if consulta in texto_normalizado:
            puntaje += 100

        if consulta_compacta in texto_compacto:
            puntaje += 90

        if tokens and all(
            token in texto_normalizado or token in texto_compacto
            for token in tokens
        ):
            puntaje += 60 + len(tokens) * 10

        if puntaje > 0:
            coincidencias.append((puntaje, item))

    coincidencias.sort(key=lambda dato: (-dato[0], dato[1].get("nombre", "")))

    return [item for _, item in coincidencias[:limite]]


def obtener_lista(valor):
    if isinstance(valor, list):
        return valor

    if valor:
        return [valor]

    return []


def obtener_primero(valor):
    lista = obtener_lista(valor)
    return quitar_html(lista[0]) if lista else ""


def limpiar_url_categoria(texto):
    texto = quitar_html(texto)

    if texto.startswith("http://dbpedia.org/resource/Category:"):
        texto = texto.replace("http://dbpedia.org/resource/Category:", "")

    if texto.startswith("https://dbpedia.org/resource/Category:"):
        texto = texto.replace("https://dbpedia.org/resource/Category:", "")

    return texto.replace("_", " ")


def limpiar_resultado_lookup(item):
    nombre = obtener_primero(
        item.get("label")
        or item.get("labelName")
        or item.get("title")
    )

    enlace = obtener_primero(
        item.get("resource")
        or item.get("uri")
        or item.get("id")
    )

    abstract = obtener_primero(
        item.get("comment")
        or item.get("description")
        or item.get("abstract")
    )

    tipos = [
        quitar_html(str(tipo)).replace("http://dbpedia.org/ontology/", "")
        for tipo in obtener_lista(
            item.get("typeName")
            or item.get("type")
            or item.get("classes")
        )
    ]

    categorias = [
        limpiar_url_categoria(categoria)
        for categoria in obtener_lista(
            item.get("category")
            or item.get("categories")
        )
    ]

    return {
        "nombre": nombre or enlace.rsplit("/", 1)[-1].replace("_", " "),
        "abstract": abstract,
        "countries": categorias[:4],
        "enlace": enlace,
        "imagen": "",
        "typeLabel": ", ".join(str(tipo) for tipo in tipos[:3]),
        "ingredientes": [],
    }


def extraer_resultados_lookup(data):
    if isinstance(data, dict):
        if isinstance(data.get("docs"), list):
            return data["docs"]

        if isinstance(data.get("results"), list):
            return data["results"]

        if isinstance(data.get("resource"), list):
            return data["resource"]

    if isinstance(data, list):
        return data

    return []


def calcular_puntaje_reposteria(resultado, termino):
    consulta = normalizar_texto(termino)
    tokens = tokenizar(termino)

    texto = normalizar_texto(" ".join([
        resultado.get("nombre", ""),
        resultado.get("abstract", ""),
        resultado.get("typeLabel", ""),
        " ".join(resultado.get("countries", [])),
    ]))

    puntaje = 0

    if consulta and consulta in texto:
        puntaje += 100

    for token in tokens:
        if token in texto:
            puntaje += 20

    for palabra in PALABRAS_REPOSTERIA:
        if palabra in texto:
            puntaje += 15

    for palabra in PALABRAS_NO_REPOSTERIA:
        if palabra in texto:
            puntaje -= 80

    return puntaje


def es_resultado_reposteria(resultado, termino):
    puntaje = calcular_puntaje_reposteria(resultado, termino)
    return puntaje >= 25


def consultar_dbpedia_online(termino, limite=6):
    consulta = normalizar_texto(termino)

    if not consulta:
        return []

    timeout = float(os.getenv("DBPEDIA_TIMEOUT", "3"))

    parametros = {
        "query": f"{consulta} dessert food recipe",
        "format": "JSON",
        "maxResults": 20,
    }

    headers = {
        "Accept": "application/json",
        "User-Agent": "BuscadorReposteriaAcademico/1.0",
    }

    try:
        respuesta = requests.get(
            DBPEDIA_LOOKUP_ENDPOINT,
            params=parametros,
            headers=headers,
            timeout=timeout,
        )

        respuesta.raise_for_status()
        data = respuesta.json()

    except Exception:
        return []

    resultados_crudos = extraer_resultados_lookup(data)
    resultados_filtrados = []

    for item in resultados_crudos:
        if not isinstance(item, dict):
            continue

        resultado = limpiar_resultado_lookup(item)

        if resultado["nombre"] and es_resultado_reposteria(resultado, termino):
            puntaje = calcular_puntaje_reposteria(resultado, termino)
            resultados_filtrados.append((puntaje, resultado))

    resultados_filtrados.sort(key=lambda dato: -dato[0])

    return [resultado for _, resultado in resultados_filtrados[:limite]]


@lru_cache(maxsize=128)
def consultar_dbpedia_online_cache(termino, limite=6):
    return consultar_dbpedia_online(termino, limite)


def consultar_dbpedia(termino, limite=6):
    consulta = normalizar_texto(termino)

    if not consulta:
        return []

    if dbpedia_online_activado():
        resultados_online = consultar_dbpedia_online_cache(consulta, limite)

        if resultados_online:
            return resultados_online

    return consultar_dbpedia_offline(consulta, limite)