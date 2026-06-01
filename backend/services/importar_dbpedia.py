from pathlib import Path
import xml.etree.ElementTree as ET

from SPARQLWrapper import SPARQLWrapper, JSON

DBPEDIA_ENDPOINT = "https://dbpedia.org/sparql"

ARCHIVO_DBPEDIA = (
    Path(__file__).resolve().parent.parent / "ontologia" / "dbpedia_local.owx"
)

OWL_NAMESPACE = "http://www.w3.org/2002/07/owl#"


def crear_owl_vacio():
    if ARCHIVO_DBPEDIA.exists():
        return

    contenido = """<?xml version="1.0"?>
<Ontology xmlns="http://www.w3.org/2002/07/owl#"
  xml:base="http://www.semanticweb.org/reposteria"
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:xml="http://www.w3.org/XML/1998/namespace"
  xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
  ontologyIRI="http://www.semanticweb.org/reposteria">

</Ontology>
"""

    ARCHIVO_DBPEDIA.write_text(contenido, encoding="utf-8")


def obtener_raiz():
    crear_owl_vacio()

    arbol = ET.parse(ARCHIVO_DBPEDIA)
    raiz = arbol.getroot()

    return arbol, raiz


def limpiar_nombre(valor):
    if not valor:
        return ""

    return (
        valor.strip()
        .replace(" ", "_")
        .replace(",", "")
        .replace("(", "")
        .replace(")", "")
        .replace("/", "_")
        .replace('"', "")
        .replace("'", "")
        .replace(":", "")
    )


def existe_individuo(raiz, nombre):
    iri = f"#{nombre}"

    for elemento in raiz.findall(f".//{{{OWL_NAMESPACE}}}NamedIndividual"):

        if (
            elemento.attrib.get("IRI") == iri
            or elemento.attrib.get("abbreviatedIRI") == iri
        ):
            return True

    return False


def declarar_individuo(raiz, nombre):
    if existe_individuo(raiz, nombre):
        return

    declaracion = ET.SubElement(raiz, "Declaration")

    ET.SubElement(declaracion, "NamedIndividual", IRI=f"#{nombre}")


def agregar_clase(raiz, individuo, clase):
    axioma = ET.SubElement(raiz, "ClassAssertion")

    ET.SubElement(axioma, "Class", IRI=f"#{clase}")

    ET.SubElement(axioma, "NamedIndividual", IRI=f"#{individuo}")


def agregar_data_property(raiz, propiedad, sujeto, valor):
    if not valor:
        return

    axioma = ET.SubElement(raiz, "DataPropertyAssertion")

    ET.SubElement(axioma, "DataProperty", IRI=f"#{propiedad}")

    ET.SubElement(axioma, "NamedIndividual", IRI=f"#{sujeto}")

    literal = ET.SubElement(axioma, "Literal")

    literal.text = str(valor)


def agregar_object_property(raiz, propiedad, sujeto, objeto):
    axioma = ET.SubElement(raiz, "ObjectPropertyAssertion")

    ET.SubElement(axioma, "ObjectProperty", IRI=f"#{propiedad}")

    ET.SubElement(axioma, "NamedIndividual", IRI=f"#{sujeto}")

    ET.SubElement(axioma, "NamedIndividual", IRI=f"#{objeto}")


def consultar_dbpedia(limite=100):
    sparql = SPARQLWrapper(DBPEDIA_ENDPOINT)

    sparql.setReturnFormat(JSON)

    sparql.setQuery(f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT DISTINCT
?resource
?label
?abstract
?thumbnail
?countryLabel
?typeLabel
?ingredientLabel

WHERE {{
    ?resource rdf:type dbo:Food .
    ?resource rdfs:label ?label .

    FILTER(LANG(?label) = "es")

    OPTIONAL {{
        ?resource dbo:abstract ?abstract .
        FILTER(LANG(?abstract) = "es")
    }}

    OPTIONAL {{
        ?resource dbo:thumbnail ?thumbnail .
    }}

    OPTIONAL {{
        ?resource dbo:country ?country .
        ?country rdfs:label ?countryLabel .

        FILTER(LANG(?countryLabel) = "es")
    }}

    OPTIONAL {{
        ?resource rdf:type ?type .
        ?type rdfs:label ?typeLabel .

        FILTER(LANG(?typeLabel) = "es")
    }}

    OPTIONAL {{
        ?resource dbo:ingredient ?ingredient .
        ?ingredient rdfs:label ?ingredientLabel .

        FILTER(LANG(?ingredientLabel) = "es")
    }}
}}
LIMIT {limite}
""")

    try:
        resultados = sparql.query().convert()
    except Exception as error:
        print("ERROR CONSULTANDO DBPEDIA")
        print(error)
        return []

    datos = {}

    for fila in resultados.get("results", {}).get("bindings", []):

        recurso = fila.get("resource", {}).get("value", "")

        label = fila.get("label", {}).get("value", "")

        abstract = fila.get("abstract", {}).get("value", "")

        thumbnail = fila.get("thumbnail", {}).get("value", "")

        country = fila.get("countryLabel", {}).get("value", "")

        type_label = fila.get("typeLabel", {}).get("value", "")

        ingredient = fila.get("ingredientLabel", {}).get("value", "")

        if recurso not in datos:

            datos[recurso] = {
                "nombre": label,
                "abstract": abstract,
                "imagen": thumbnail,
                "countries": [],
                "types": [],
                "ingredientes": [],
                "recurso": recurso,
            }

        if country and country not in datos[recurso]["countries"]:
            datos[recurso]["countries"].append(country)

        if ingredient and ingredient not in datos[recurso]["ingredientes"]:
            datos[recurso]["ingredientes"].append(ingredient)

        if type_label and type_label not in datos[recurso]["types"]:
            datos[recurso]["types"].append(type_label)

    return list(datos.values())


def importar_recurso(raiz, recurso):
    nombre = limpiar_nombre(recurso["nombre"])

    declarar_individuo(raiz, nombre)

    agregar_clase(raiz, nombre, "PostreDBpedia")

    agregar_data_property(raiz, "descripcion", nombre, recurso.get("abstract", ""))

    agregar_data_property(raiz, "imagen", nombre, recurso.get("imagen", ""))

    agregar_data_property(raiz, "enlaceDBpedia", nombre, recurso.get("recurso", ""))

    for pais in recurso.get("countries", []):

        pais_limpio = limpiar_nombre(pais)

        declarar_individuo(raiz, pais_limpio)

        agregar_clase(raiz, pais_limpio, "Pais")

        agregar_object_property(raiz, "tienePais", nombre, pais_limpio)

    for ingrediente in recurso.get("ingredientes", []):

        ingrediente_limpio = limpiar_nombre(ingrediente)

        declarar_individuo(raiz, ingrediente_limpio)

        agregar_clase(raiz, ingrediente_limpio, "Ingrediente")

        agregar_object_property(raiz, "tieneIngrediente", nombre, ingrediente_limpio)

    for tipo in recurso.get("types", []):

        tipo_limpio = limpiar_nombre(tipo)

        declarar_individuo(raiz, tipo_limpio)

        agregar_clase(raiz, tipo_limpio, "TipoSemantico")

        agregar_object_property(raiz, "tieneTipo", nombre, tipo_limpio)


def poblar_ontologia():
    print("Consultando DBPedia...")

    resultados = consultar_dbpedia(limite=100)

    print(f"Recursos obtenidos: {len(resultados)}")

    arbol, raiz = obtener_raiz()

    for recurso in resultados:

        importar_recurso(raiz, recurso)

    arbol.write(ARCHIVO_DBPEDIA, encoding="utf-8", xml_declaration=True)

    print("Ontología poblada correctamente.")
    print(ARCHIVO_DBPEDIA)


if __name__ == "__main__":
    poblar_ontologia()
