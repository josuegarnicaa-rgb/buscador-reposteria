export type Resumen = {
  clases: number
  propiedades_objeto: number
  propiedades_datos: number
  individuos: number
}

export type Resultado = {
  nombre: string
  tipo: string
  clases: string[]
  superclases: string[]
  atributos: Record<string, string[]>
  relaciones: Record<string, string[]>
  usado_en: Record<string, string[]>
}

export type BusquedaResponse = {
  resultados: Resultado[]
}

