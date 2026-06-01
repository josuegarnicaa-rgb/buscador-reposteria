from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

from services.i18n import (
    normalizar_idioma,
    normalizar_texto,
    traducir_identificador,
    traducir_lista,
    traducir_origen,
)

ARCHIVO_DBPEDIA_LOCAL = (
    Path(__file__).resolve().parent.parent / "ontologia" / "dbpedia_local.owx"
)


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


def cargar_dbpedia_local():
    if not ARCHIVO_DBPEDIA_LOCAL.exists():
        return {}

    arbol = ET.parse(ARCHIVO_DBPEDIA_LOCAL)
    raiz = arbol.getroot()

    clases_individuo = defaultdict(set)

    for axioma in raiz:
        if nombre_xml(axioma) != "ClassAssertion":
            continue

        hijos = list(axioma)
        if len(hijos) < 2:
            continue

        clase = obtener_iri(hijos[0])
        individuo = obtener_iri(hijos[1])

        if clase and individuo:
            clases_individuo[individuo].add(clase)

    datos = {}

    for axioma in raiz:
        tipo_axioma = nombre_xml(axioma)
        hijos = list(axioma)

        if tipo_axioma == "DataPropertyAssertion" and len(hijos) >= 3:
            propiedad = obtener_iri(hijos[0])
            sujeto = obtener_iri(hijos[1])
            valor = "".join(hijos[2].itertext()).strip()

            if not sujeto or "PostreDBpedia" not in clases_individuo.get(sujeto, set()):
                continue

            if sujeto not in datos:
                datos[sujeto] = {
                    "id": sujeto,
                    "nombre": sujeto,
                    "abstract": "",
                    "countries": [],
                    "enlace": "",
                    "imagen": "",
                    "typeLabel": [],
                    "ingredientes": [],
                    "origen": "DBPEDIA LOCAL",
                }

            if propiedad == "imagen":
                datos[sujeto]["imagen"] = valor
            elif propiedad == "enlaceDBpedia":
                datos[sujeto]["enlace"] = valor
            elif propiedad in {"descripcion", "abstract"}:
                datos[sujeto]["abstract"] = valor

        elif tipo_axioma == "ObjectPropertyAssertion" and len(hijos) >= 3:
            propiedad = obtener_iri(hijos[0])
            sujeto = obtener_iri(hijos[1])
            objeto = obtener_iri(hijos[2])

            if not sujeto or "PostreDBpedia" not in clases_individuo.get(sujeto, set()):
                continue

            if sujeto not in datos:
                datos[sujeto] = {
                    "id": sujeto,
                    "nombre": sujeto,
                    "abstract": "",
                    "countries": [],
                    "enlace": "",
                    "imagen": "",
                    "typeLabel": [],
                    "ingredientes": [],
                    "origen": "DBPEDIA LOCAL",
                }

            if propiedad == "tienePais" and objeto not in datos[sujeto]["countries"]:
                datos[sujeto]["countries"].append(objeto)
            elif (
                propiedad == "tieneIngrediente"
                and objeto not in datos[sujeto]["ingredientes"]
            ):
                datos[sujeto]["ingredientes"].append(objeto)
            elif propiedad == "tieneTipo" and objeto not in datos[sujeto]["typeLabel"]:
                datos[sujeto]["typeLabel"].append(objeto)

    return datos


DBPEDIA_LOCAL = cargar_dbpedia_local()


def texto_busqueda_recurso_local(recurso, idioma):
    partes = [
        recurso["nombre"],
        traducir_identificador(recurso["nombre"], idioma),
        recurso.get("abstract", ""),
        recurso.get("enlace", ""),
        traducir_lista(recurso.get("countries", []), idioma),
        traducir_lista(recurso.get("ingredientes", []), idioma),
        traducir_lista(recurso.get("typeLabel", []), idioma),
    ]

    aplanado = []
    for parte in partes:
        if isinstance(parte, list):
            aplanado.extend(parte)
        else:
            aplanado.append(parte)

    return normalizar_texto(" ".join(aplanado))


def traducir_recurso_local(recurso, idioma):
    tipo_label = traducir_lista(recurso.get("typeLabel", []), idioma)

    return {
        "id": recurso["id"],
        "nombre": traducir_identificador(recurso["nombre"], idioma),
        "abstract": traducir_identificador(recurso.get("abstract", ""), idioma),
        "countries": traducir_lista(recurso.get("countries", []), idioma),
        "enlace": recurso.get("enlace", ""),
        "imagen": recurso.get("imagen", ""),
        "typeLabel": ", ".join(tipo_label),
        "ingredientes": traducir_lista(recurso.get("ingredientes", []), idioma),
        "origen": traducir_origen(recurso.get("origen", "DBPEDIA LOCAL"), idioma),
    }


def buscar_dbpedia_local(termino, idioma="es", limite=6):
    idioma = normalizar_idioma(idioma)
    consulta = normalizar_texto(termino)

    if not consulta:
        return []

    resultados = []

    for recurso in DBPEDIA_LOCAL.values():
        if consulta in texto_busqueda_recurso_local(recurso, idioma):
            resultados.append(traducir_recurso_local(recurso, idioma))

        if len(resultados) >= limite:
            break

    return resultados

