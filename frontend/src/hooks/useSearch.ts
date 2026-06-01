import { useState } from 'react'
import type { BusquedaResponse, Idioma } from '../types'
import { API_BASE_URL } from '../config'
import { obtenerTextos } from '../i18n'

export const useSearch = (idioma: Idioma) => {
  const [resultados, setResultados] = useState<BusquedaResponse | null>(null)
  const [buscado, setBuscado] = useState('')
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  const buscar = async (valor: string, idiomaBusqueda = idioma) => {
    const consulta = valor.trim()

    if (!consulta) {
      setResultados(null)
      setBuscado('')
      setError('')
      return
    }

    setCargando(true)
    setError('')

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/buscar?termino=${encodeURIComponent(consulta)}&idioma=${idiomaBusqueda}`,
      )

      if (!response.ok) {
        throw new Error('La búsqueda falló')
      }

      const data = (await response.json()) as BusquedaResponse
      setResultados(data)
      setBuscado(consulta)
    } catch {
      setError(obtenerTextos(idiomaBusqueda).errorBusqueda)
    } finally {
      setCargando(false)
    }
  }

  return {
    buscar,
    resultados,
    buscado,
    cargando,
    error,
  }
}
