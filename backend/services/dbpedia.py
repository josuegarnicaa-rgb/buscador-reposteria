from SPARQLWrapper import SPARQLWrapper, JSON

from services.i18n import normalizar_idioma

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


def _normalizar_termino(termino):
    return termino.strip().lower().replace('"', "").replace("'", "")


def consultar_dbpedia(termino, idioma='es', limite=6):
    consulta = _normalizar_termino(termino)
    idioma = normalizar_idioma(idioma)

    if not consulta:
        return []

    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT ?resource ?label ?abstract ?thumbnail ?countryLabel ?typeLabel ?ingredientLabel WHERE {{

    ?resource rdf:type dbo:Food .
    ?resource rdfs:label ?label .

    FILTER(LANGMATCHES(LANG(?label), "{idioma}"))
    FILTER(CONTAINS(LCASE(STR(?label)), "{consulta}"))

    OPTIONAL {{
        ?resource dbo:abstract ?abstract .
        FILTER(LANGMATCHES(LANG(?abstract), "{idioma}"))
    }}

    OPTIONAL {{
        ?resource dbo:thumbnail ?thumbnail .
    }}

    OPTIONAL {{
        ?resource dbo:country ?country .
        ?country rdfs:label ?countryLabel .

        FILTER(LANGMATCHES(LANG(?countryLabel), "{idioma}"))
    }}
    OPTIONAL {{
        ?resource rdf:type ?type .
        ?type rdfs:label ?typeLabel .

        FILTER(LANGMATCHES(LANG(?typeLabel), "{idioma}"))
    }}

    OPTIONAL {{
        ?resource dbo:ingredient ?ingredient .
        ?ingredient rdfs:label ?ingredientLabel .

        FILTER(LANGMATCHES(LANG(?ingredientLabel), "{idioma}"))
    }}
}}
LIMIT {limite}
        """)

    try:
        resultados = sparql.query().convert()
    except Exception:
        return []

    datos = {}

    for fila in resultados.get("results", {}).get("bindings", []):

        recurso = fila.get("resource", {}).get("value", "")
        label = fila.get("label", {}).get("value", "")
        abstract = fila.get("abstract", {}).get("value", "")
        thumbnail = fila.get("thumbnail", {}).get("value", "")
        country = fila.get("countryLabel", {}).get("value", "")
        typeLabel = fila.get("typeLabel", {}).get("value", "")
        ingredient = fila.get("ingredientLabel", {}).get("value", "")

        if recurso not in datos:
            datos[recurso] = {
                "nombre": label or recurso.rsplit("/", 1)[-1],
                "abstract": abstract,
                "countries": [],
                "enlace": recurso,
                "imagen": thumbnail,
                "typeLabel": typeLabel,
                "ingredientes": [],
            }

        if ingredient and ingredient not in datos[recurso]["ingredientes"]:
            datos[recurso]["ingredientes"].append(ingredient)

        if country and country not in datos[recurso]["countries"]:
            datos[recurso]["countries"].append(country)

    return list(datos.values())
