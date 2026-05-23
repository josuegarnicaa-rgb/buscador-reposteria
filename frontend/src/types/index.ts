export type Resumen = {
  clases: number
  propiedades_objeto: number
  propiedades_datos: number
  individuos: number
}

export type Resultado = {
  nombre: string
  tipo: string
  fuente?: string
  clases: string[]
  superclases: string[]
  atributos: Record<string, string[]>
  relaciones: Record<string, string[]>
  usado_en: Record<string, string[]>
  descripcion?: string
  enlace?: string
  imagen?: string
}

export type BusquedaResponse = {
  termino?: string
  resultados: Resultado[]
  fuentes?: {
    local: number
    dbpedia: number
  }
}

