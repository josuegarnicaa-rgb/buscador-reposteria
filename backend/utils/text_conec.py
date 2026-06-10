_CONECTORES_ES = {
    "de",
    "del",
    "la",
    "el",
    "los",
    "las",
    "un",
    "una",
    "unos",
    "unas",
    "y",
    "o",
    "e",
    "u",
    "a",
    "en",
    "con",
    "sin",
    "por",
    "para",
    "que",
    "al",
    "lo",
    "se",
    "su",
    "sus",
}


def quitar_conectores(texto: str) -> str:
    palabras = texto.split()
    filtradas = [p for p in palabras if p.lower() not in _CONECTORES_ES]
    return " ".join(filtradas)
