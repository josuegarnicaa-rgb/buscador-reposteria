import type { Idioma } from './types'

type TextosInterfaz = {
  navBadge: string
  navTitle: string
  summaryClases: string
  summaryObjectProperties: string
  summaryDataProperties: string
  summaryIndividuos: string
  languageLabel: string
  languageHelp: string
  searchPlaceholder: string
  searchButton: string
  searchingButton: string
  resultsFor: string
  resultsFoundSingular: string
  resultsFoundPlural: string
  noResults: string
  localResultsHeading: string
  dbpediaRemoteHeading: string
  dbpediaLocalHeading: string
  elementPrefix: string
  typeLabel: string
  classesLabel: string
  superclassesLabel: string
  relationsLabel: string
  attributesLabel: string
  usedInLabel: string
  countriesLabel: string
  ingredientsLabel: string
  noImageLabel: string
  sourceLabel: string
  sourceButton: string
  errorBusqueda: string
  errorResumen: string
}

export const idiomasDisponibles: Array<{ value: Idioma; label: string }> = [
  { value: 'es', label: 'Español' },
  { value: 'en', label: 'English' },
  { value: 'pt', label: 'Português' },
  { value: 'fr', label: 'Français' },
  { value: 'it', label: 'Italiano' },
]

const textos: Record<Idioma, TextosInterfaz> = {
  es: {
    navBadge: 'Buscador semántico de repostería',
    navTitle: 'Consulta productos, recetas, ingredientes, herramientas y relaciones de la ontología.',
    summaryClases: 'Clases',
    summaryObjectProperties: 'Propiedades de objeto',
    summaryDataProperties: 'Propiedades de datos',
    summaryIndividuos: 'Individuos',
    languageLabel: 'Idioma',
    languageHelp: 'La búsqueda y los resultados se presentarán en el idioma elegido.',
    searchPlaceholder: 'Buscar: chocolate, torta, huevo, receta...',
    searchButton: 'Buscar',
    searchingButton: 'Buscando...',
    resultsFor: 'Resultados para',
    resultsFoundSingular: 'coincidencia encontrada',
    resultsFoundPlural: 'coincidencias encontradas',
    noResults: 'No se encontraron resultados.',
    localResultsHeading: 'Ontología local',
    dbpediaRemoteHeading: 'DBpedia remota',
    dbpediaLocalHeading: 'DBpedia local',
    elementPrefix: 'Elemento',
    typeLabel: 'Tipo',
    classesLabel: 'Clases',
    superclassesLabel: 'Superclases',
    relationsLabel: 'Relaciones semánticas',
    attributesLabel: 'Atributos',
    usedInLabel: 'Usado en',
    countriesLabel: 'Países',
    ingredientsLabel: 'Ingredientes',
    noImageLabel: 'Sin imagen disponible para este resultado',
    sourceLabel: 'Fuente: DBpedia',
    sourceButton: 'Ver fuente',
    errorBusqueda: 'Ocurrió un error al realizar la búsqueda.',
    errorResumen: 'Ocurrió un error al obtener el resumen.',
  },
  en: {
    navBadge: 'Semantic search engine for pastry',
    navTitle: 'Consult products, recipes, ingredients, tools, and relationships of ontology.',
    summaryClases: 'Classes',
    summaryObjectProperties: 'Object Properties',
    summaryDataProperties: 'Data Properties',
    summaryIndividuos: 'Individuals',
    languageLabel: 'Language',
    languageHelp: 'The search and results will be presented in the chosen language.',
    searchPlaceholder: 'Search: chocolate, cake, egg, recipe...',
    searchButton: 'Search',
    searchingButton: 'Searching...',
    resultsFor: 'Results for',
    resultsFoundSingular: 'match found',
    resultsFoundPlural: 'matches found',
    noResults: 'No results found.',
    localResultsHeading: 'Local ontology',
    dbpediaRemoteHeading: 'Remote DBpedia',
    dbpediaLocalHeading: 'Local DBpedia',
    elementPrefix: 'Item',
    typeLabel: 'Type',
    classesLabel: 'Classes',
    superclassesLabel: 'Superclasses',
    relationsLabel: 'Semantic relationships',
    attributesLabel: 'Attributes',
    usedInLabel: 'Used in',
    countriesLabel: 'Countries',
    ingredientsLabel: 'Ingredients',
    noImageLabel: 'No image available for this result',
    sourceLabel: 'Source: DBpedia',
    sourceButton: 'Open source',
    errorBusqueda: 'An error occurred while searching.',
    errorResumen: 'An error occurred while loading the summary.',
  },
  pt: {
    navBadge: 'Mecanismo de busca semântica para confeitaria',
    navTitle: 'Consulte produtos, receitas, ingredientes, ferramentas e relações de ontologia.',
    summaryClases: 'Classes',
    summaryObjectProperties: 'Propriedades do objeto',
    summaryDataProperties: 'Propriedades do dados',
    summaryIndividuos: 'Indivíduos',
    languageLabel: 'Linguagem',
    languageHelp: 'A pesquisa e os resultados serão apresentados no idioma escolhido.',
    searchPlaceholder: 'Buscar: chocolate, bolo, ovo, receita...',
    searchButton: 'Buscar',
    searchingButton: 'Buscando...',
    resultsFor: 'Resultados para',
    resultsFoundSingular: 'correspondência encontrada',
    resultsFoundPlural: 'correspondências encontradas',
    noResults: 'Nenhum resultado encontrado.',
    localResultsHeading: 'Ontologia local',
    dbpediaRemoteHeading: 'DBpedia remota',
    dbpediaLocalHeading: 'DBpedia local',
    elementPrefix: 'Item',
    typeLabel: 'Tipo',
    classesLabel: 'Classes',
    superclassesLabel: 'Superclasses',
    relationsLabel: 'Relações semânticas',
    attributesLabel: 'Atributos',
    usedInLabel: 'Usado em',
    countriesLabel: 'Países',
    ingredientsLabel: 'Ingredientes',
    noImageLabel: 'Nenhuma imagem disponível para este resultado',
    sourceLabel: 'Fonte: DBpedia',
    sourceButton: 'Abrir fonte',
    errorBusqueda: 'Ocorreu um erro ao realizar a busca.',
    errorResumen: 'Ocorreu um erro ao carregar o resumo.',
  },
  fr: {
    navBadge: 'Moteur de recherche sémantique pour la pâtisserie',
    navTitle: "Consultez les produits, les recettes, les ingrédients, les outils et les relations de l'ontologie.",
    summaryClases: 'Classes',
    summaryObjectProperties: "Propriétés de l'objet",
    summaryDataProperties: 'Propriétés de données',
    summaryIndividuos: 'Individus',
    languageLabel: 'Langue',
    languageHelp: 'La recherche et les résultats seront présentés dans la langue choisie.',
    searchPlaceholder: 'Rechercher: chocolat, gâteau, œuf, recette...',
    searchButton: 'Rechercher',
    searchingButton: 'Recherche...',
    resultsFor: 'Résultats pour',
    resultsFoundSingular: 'correspondance trouvée',
    resultsFoundPlural: 'correspondances trouvées',
    noResults: 'Aucun résultat trouvé.',
    localResultsHeading: 'Ontologie locale',
    dbpediaRemoteHeading: 'DBpedia distante',
    dbpediaLocalHeading: 'DBpedia locale',
    elementPrefix: 'Élément',
    typeLabel: 'Type',
    classesLabel: 'Classes',
    superclassesLabel: 'Superclasses',
    relationsLabel: 'Relations sémantiques',
    attributesLabel: 'Attributs',
    usedInLabel: 'Utilisé dans',
    countriesLabel: 'Pays',
    ingredientsLabel: 'Ingrédients',
    noImageLabel: 'Aucune image disponible pour ce résultat',
    sourceLabel: 'Source : DBpedia',
    sourceButton: 'Voir la source',
    errorBusqueda: 'Une erreur est survenue lors de la recherche.',
    errorResumen: 'Une erreur est survenue lors du chargement du résumé.',
  },
  it: {
    navBadge: 'Motore di ricerca semantico per pasticceria',
    navTitle: 'Consultare prodotti, ricette, ingredienti, strumenti e relazioni ontologiche.',
    summaryClases: 'Classes',
    summaryObjectProperties: "Proprietà dell'oggetto",
    summaryDataProperties: "Proprietà dei dati",
    summaryIndividuos: 'Individui',
    languageLabel: 'Lingua',
    languageHelp: 'La ricerca e i risultati saranno presentati nella lingua selezionata.',
    searchPlaceholder: 'Cerca: cioccolato, torta, uovo, ricetta...',
    searchButton: 'Cerca',
    searchingButton: 'Ricerca...',
    resultsFor: 'Risultati per',
    resultsFoundSingular: 'corrispondenza trovata',
    resultsFoundPlural: 'corrispondenze trovate',
    noResults: 'Nessun risultato trovato.',
    localResultsHeading: 'Ontologia locale',
    dbpediaRemoteHeading: 'DBpedia remota',
    dbpediaLocalHeading: 'DBpedia locale',
    elementPrefix: 'Elemento',
    typeLabel: 'Tipo',
    classesLabel: 'Classi',
    superclassesLabel: 'Superclassi',
    relationsLabel: 'Relazioni semantiche',
    attributesLabel: 'Attributi',
    usedInLabel: 'Usato in',
    countriesLabel: 'Paesi',
    ingredientsLabel: 'Ingredienti',
    noImageLabel: 'Nessuna immagine disponibile per questo risultato',
    sourceLabel: 'Fonte: DBpedia',
    sourceButton: 'Apri fonte',
    errorBusqueda: 'Si è verificato un errore durante la ricerca.',
    errorResumen: 'Si è verificato un errore durante il caricamento del riepilogo.',
  },
}

export const obtenerTextos = (idioma: Idioma) => textos[idioma] ?? textos.es
