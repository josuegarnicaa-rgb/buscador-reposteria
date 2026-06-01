import re
import unicodedata

IDIOMAS_VALIDOS = {'es', 'en', 'pt', 'fr', 'it'}
IDIOMA_POR_DEFECTO = 'es'

TRADUCCIONES = {
    'animal': {'es': 'animal', 'en': 'animal', 'pt': 'animal', 'fr': 'animal', 'it': 'animale'},
    'azucar': {'es': 'azúcar', 'en': 'sugar', 'pt': 'açúcar', 'fr': 'sucre', 'it': 'zucchero'},
    'brownie': {'es': 'brownie', 'en': 'brownie', 'pt': 'brownie', 'fr': 'brownie', 'it': 'brownie'},
    'cheesecake': {'es': 'cheesecake', 'en': 'cheesecake', 'pt': 'cheesecake', 'fr': 'cheesecake', 'it': 'cheesecake'},
    'clase': {'es': 'clase', 'en': 'class', 'pt': 'classe', 'fr': 'classe', 'it': 'classe'},
    'decoracion': {'es': 'decoración', 'en': 'decoration', 'pt': 'decoração', 'fr': 'décoration', 'it': 'decorazione'},
    'dona': {'es': 'dona', 'en': 'doughnut', 'pt': 'donut', 'fr': 'beignet', 'it': 'ciambella'},
    'cupcake': {'es': 'cupcake', 'en': 'cupcake', 'pt': 'cupcake', 'fr': 'cupcake', 'it': 'cupcake'},
    'durazno': {'es': 'durazno', 'en': 'peach', 'pt': 'pêssego', 'fr': 'pêche', 'it': 'pesca'},
    'evento': {'es': 'evento', 'en': 'event', 'pt': 'evento', 'fr': 'événement', 'it': 'evento'},
    'fresa': {'es': 'fresa', 'en': 'strawberry', 'pt': 'morango', 'fr': 'fraise', 'it': 'fragola'},
    'fruta': {'es': 'fruta', 'en': 'fruit', 'pt': 'fruta', 'fr': 'fruit', 'it': 'frutta'},
    'galleta': {'es': 'galleta', 'en': 'cookie', 'pt': 'biscoito', 'fr': 'biscuit', 'it': 'biscotto'},
    'gluten': {'es': 'gluten', 'en': 'gluten', 'pt': 'glúten', 'fr': 'gluten', 'it': 'glutine'},
    'herramienta': {'es': 'herramienta', 'en': 'tool', 'pt': 'ferramenta', 'fr': 'outil', 'it': 'strumento'},
    'individual': {'es': 'individuo', 'en': 'individual', 'pt': 'indivíduo', 'fr': 'individu', 'it': 'individuo'},
    'individuo': {'es': 'individuo', 'en': 'individual', 'pt': 'indivíduo', 'fr': 'individu', 'it': 'individuo'},
    'ingrediente': {'es': 'ingrediente', 'en': 'ingredient', 'pt': 'ingrediente', 'fr': 'ingrédient', 'it': 'ingrediente'},
    'liquido': {'es': 'líquido', 'en': 'liquid', 'pt': 'líquido', 'fr': 'liquide', 'it': 'liquido'},
    'muffin': {'es': 'muffin', 'en': 'muffin', 'pt': 'muffin', 'fr': 'muffin', 'it': 'muffin'},
    'pastry': {'es': 'repostería', 'en': 'pastry', 'pt': 'confeitaria', 'fr': 'pâtisserie', 'it': 'pasticceria'},
    'pie': {'es': 'pie', 'en': 'pie', 'pt': 'torta', 'fr': 'tarte', 'it': 'torta'},
    'principal': {'es': 'principal', 'en': 'main', 'pt': 'principal', 'fr': 'principal', 'it': 'principale'},
    'producto': {'es': 'producto', 'en': 'product', 'pt': 'produto', 'fr': 'produit', 'it': 'prodotto'},
    'pudin': {'es': 'pudín', 'en': 'pudding', 'pt': 'pudim', 'fr': 'pudding', 'it': 'budino'},
    'receta': {'es': 'receta', 'en': 'recipe', 'pt': 'receita', 'fr': 'recette', 'it': 'ricetta'},
    'refrigeracion': {'es': 'refrigeración', 'en': 'refrigeration', 'pt': 'refrigeração', 'fr': 'réfrigération', 'it': 'refrigerazione'},
    'relleno': {'es': 'relleno', 'en': 'filling', 'pt': 'recheio', 'fr': 'garniture', 'it': 'ripieno'},
    'reposteria': {'es': 'repostería', 'en': 'pastry', 'pt': 'confeitaria', 'fr': 'pâtisserie', 'it': 'pasticceria'},
    'sabor': {'es': 'sabor', 'en': 'flavor', 'pt': 'sabor', 'fr': 'saveur', 'it': 'sapore'},
    'seco': {'es': 'seco', 'en': 'dry', 'pt': 'seco', 'fr': 'sec', 'it': 'secco'},
    'sin': {'es': 'sin', 'en': 'without', 'pt': 'sem', 'fr': 'sans', 'it': 'senza'},
    'superclase': {'es': 'superclase', 'en': 'superclass', 'pt': 'superclasse', 'fr': 'superclasse', 'it': 'superclasse'},
    'tamaño': {'es': 'tamaño', 'en': 'size', 'pt': 'tamanho', 'fr': 'taille', 'it': 'dimensione'},
    'temperatura': {'es': 'temperatura', 'en': 'temperature', 'pt': 'temperatura', 'fr': 'température', 'it': 'temperatura'},
    'tiempo': {'es': 'tiempo', 'en': 'time', 'pt': 'tempo', 'fr': 'temps', 'it': 'tempo'},
    'tipo': {'es': 'tipo', 'en': 'type', 'pt': 'tipo', 'fr': 'type', 'it': 'tipo'},
    'torta': {'es': 'torta', 'en': 'cake', 'pt': 'bolo', 'fr': 'gâteau', 'it': 'torta'},
    'usar': {'es': 'usar', 'en': 'use', 'pt': 'usar', 'fr': 'utiliser', 'it': 'usare'},
    'usa': {'es': 'usa', 'en': 'uses', 'pt': 'usa', 'fr': 'utilise', 'it': 'usa'},
    'vegetal': {'es': 'vegetal', 'en': 'vegetable', 'pt': 'vegetal', 'fr': 'végétal', 'it': 'vegetale'},
    'vainilla': {'es': 'vainilla', 'en': 'vanilla', 'pt': 'baunilha', 'fr': 'vanille', 'it': 'vaniglia'},
    'zanahoria': {'es': 'zanahoria', 'en': 'carrot', 'pt': 'cenoura', 'fr': 'carotte', 'it': 'carota'},
}


def normalizar_idioma(idioma):
    idioma_normalizado = (idioma or '').strip().lower()
    if idioma_normalizado in IDIOMAS_VALIDOS:
        return idioma_normalizado
    return IDIOMA_POR_DEFECTO


def normalizar_texto(texto):
    texto_normalizado = unicodedata.normalize('NFKD', texto or '')
    sin_tildes = ''.join(
        caracter for caracter in texto_normalizado if not unicodedata.combining(caracter)
    )
    return sin_tildes.lower()


def separar_identificador(valor):
    limpio = (valor or '').replace('#', ' ').replace('_', ' ').replace('-', ' ')
    limpio = re.sub(r'(?<=[a-záéíóúñ])(?=[A-ZÁÉÍÓÚÑ])', ' ', limpio)
    limpio = re.sub(r'(?<=[A-Za-z])(?=\d)', ' ', limpio)
    limpio = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', limpio)
    return [parte for parte in limpio.split() if parte]


def traducir_palabra(palabra, idioma):
    clave = normalizar_texto(palabra)
    return TRADUCCIONES.get(clave, {}).get(idioma, palabra)


def traducir_texto(texto, idioma):
    partes = separar_identificador(texto)
    if not partes:
        return texto
    traduccion = ' '.join(traducir_palabra(parte, idioma) for parte in partes)
    return traduccion[:1].upper() + traduccion[1:] if traduccion else texto


def traducir_identificador(identificador, idioma):
    return traducir_texto(identificador, idioma)


def traducir_lista(valores, idioma):
    return [traducir_identificador(valor, idioma) for valor in valores]


def traducir_mapa(valores, idioma):
    return {
        traducir_identificador(clave, idioma): traducir_lista(valores_clave, idioma)
        for clave, valores_clave in valores.items()
    }