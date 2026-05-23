from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"


def _normalizar_termino(termino):
    return termino.strip().lower().replace('"', "").replace("'", "")


def consultar_dbpedia(termino, limite=6):
    consulta = _normalizar_termino(termino)

    if not consulta:
        return []

    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX dbo: <http://dbpedia.org/ontology/>

        SELECT DISTINCT ?resource ?label ?abstract ?thumbnail ?country WHERE {{
                    ?resource rdfs:label ?label .
          FILTER (LANG(?label) IN ("en", "es"))
          FILTER (CONTAINS(LCASE(STR(?label)), "{consulta}"))
                    OPTIONAL {{
                        ?resource dbo:abstract ?abstract .
                        FILTER (LANG(?abstract) IN ("en", "es"))
                    }}
                    OPTIONAL {{ ?resource dbo:thumbnail ?thumbnail . }}
                    OPTIONAL {{ ?resource dbo:country ?country . }}
        }}
        LIMIT {limite}
        """)

    try:
        resultados = sparql.query().convert()
    except Exception:
        return []

    datos = []

    for fila in resultados.get("results", {}).get("bindings", []):
        recurso = fila.get("resource", {}).get("value", "")
        label = fila.get("label", {}).get("value", "")
        abstract = fila.get("abstract", {}).get("value", "")
        thumbnail = fila.get("thumbnail", {}).get("value", "")
        country = fila.get("country", {}).get("value", "")

        datos.append(
            {
                "nombre": label or recurso.rsplit("/", 1)[-1],
                "tipo": "DBpedia",
                "fuente": "dbpedia",
                "clases": [],
                "superclases": [],
                "atributos": {
                    "abstract": [abstract] if abstract else [],
                    "country": [country] if country else [],
                },
                "relaciones": {},
                "usado_en": {},
                "descripcion": abstract,
                "enlace": recurso,
                "imagen": thumbnail,
            }
        )

    print(f"DBpedia '{consulta}': {len(datos)} resultados")

    return datos
