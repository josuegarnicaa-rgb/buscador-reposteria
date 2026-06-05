export type Resumen = {
  clases: number
  propiedades_objeto: number
  propiedades_datos: number
  individuos: number
}

export type Idioma = 'es' | 'en' | 'pt' | 'fr' | 'it'

export type DBpedia = {
  id: string
  abstract: string
  countries: string[]
  enlace: string
  imagen: string
  nombre: string
  typeLabel: string
  ingredientes: string[]
  origen: string
}

export type Resultado = {
  id: string
  nombre: string
  tipo: string
  clases: string[]
  superclases: string[]
  atributos: Record<string, string[]>
  relaciones: Record<string, string[]>
  usado_en: Record<string, string[]>
  origen: string
}

export type BusquedaResponse = {
  resultados: Resultado[]
  dbpedia: DBpedia[]
  dbpedia_local: DBpedia[]
  total: number
}

