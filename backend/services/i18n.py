import json
import re
import unicodedata
from pathlib import Path
from deep_translator import GoogleTranslator

IDIOMAS_VALIDOS = {"es", "en", "pt", "fr", "it"}
IDIOMA_POR_DEFECTO = "es"

ORIGENES = {
    "LOCAL": {
        "es": "LOCAL",
        "en": "LOCAL",
        "pt": "LOCAL",
        "fr": "LOCAL",
        "it": "LOCALE",
    },
    "DBPEDIA REMOTO": {
        "es": "DBPEDIA REMOTO",
        "en": "REMOTE DBPEDIA",
        "pt": "DBPEDIA REMOTA",
        "fr": "DBPEDIA DISTANTE",
        "it": "DBPEDIA REMOTA",
    },
    "DBPEDIA LOCAL": {
        "es": "DBPEDIA LOCAL",
        "en": "LOCAL DBPEDIA",
        "pt": "DBPEDIA LOCAL",
        "fr": "DBPEDIA LOCALE",
        "it": "DBPEDIA LOCALE",
    },
}

_CACHE_PATH = Path(__file__).resolve().parent.parent / "cache" / "traducciones.json"
_cache_traduccion: dict[str, str] = {}


def _clave(texto: str, origen: str, destino: str) -> str:
    return f"{origen}|{destino}|{texto}"


def _cargar_cache():
    global _cache_traduccion
    if _CACHE_PATH.exists():
        try:
            _cache_traduccion = json.loads(_CACHE_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            _cache_traduccion = {}
    else:
        _cache_traduccion = {}


def _guardar_cache():
    try:
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        _CACHE_PATH.write_text(
            json.dumps(_cache_traduccion, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except OSError:
        pass


_cargar_cache()


def normalizar_idioma(idioma):
    idioma_normalizado = (idioma or "").strip().lower()
    if idioma_normalizado in IDIOMAS_VALIDOS:
        return idioma_normalizado
    return IDIOMA_POR_DEFECTO


def normalizar_texto(texto):
    texto_normalizado = unicodedata.normalize("NFKD", texto or "")
    sin_tildes = "".join(
        caracter
        for caracter in texto_normalizado
        if not unicodedata.combining(caracter)
    )
    return sin_tildes.lower()


def separar_identificador(valor):
    limpio = (valor or "").replace("#", " ").replace("_", " ").replace("-", " ")
    limpio = re.sub(r"(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])", " ", limpio)
    limpio = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", limpio)
    limpio = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", limpio)
    return [parte for parte in limpio.split() if parte]


def _traducir_con_api(texto: str, origen: str, destino: str) -> str:
    if not texto or not texto.strip():
        return texto

    clave = _clave(texto.strip(), origen, destino)

    if clave in _cache_traduccion:
        return _cache_traduccion[clave]

    try:
        resultado = GoogleTranslator(source=origen, target=destino).translate(
            texto.strip()
        )
        _cache_traduccion[clave] = resultado or texto
        _guardar_cache()
        return _cache_traduccion[clave]
    except Exception:
        return texto


def traducir_al_esp(termino: str, idioma_origen: str) -> str:
    if idioma_origen == "es":
        return termino
    return _traducir_con_api(termino, idioma_origen, "es")


def traducir_identificador(identificador: str, idioma: str) -> str:
    partes = separar_identificador(identificador)
    texto_es = " ".join(partes)

    if not texto_es:
        return identificador

    if idioma == "es":
        resultado = texto_es
    else:
        resultado = _traducir_con_api(texto_es, "es", idioma)

    return resultado[:1].upper() + resultado[1:] if resultado else identificador


def traducir_lista(valores: list, idioma: str) -> list:
    return [traducir_identificador(v, idioma) for v in valores]


def traducir_mapa(valores: dict, idioma: str) -> dict:
    return {
        traducir_identificador(clave, idioma): traducir_lista(vals, idioma)
        for clave, vals in valores.items()
    }


def traducir_origen(origen: str, idioma: str) -> str:
    idioma = normalizar_idioma(idioma)
    return ORIGENES.get(origen, {}).get(idioma, origen)
