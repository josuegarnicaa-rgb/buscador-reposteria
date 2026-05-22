import { useState } from 'react'
import type { BusquedaResponse, Resultado } from '../types'
import { API_BASE_URL } from '../config'

export const useSearch = () => {
  const [resultados, setResultados] = useState<Resultado[]>([])
  const [buscado, setBuscado] = useState('')
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  const buscar = async (valor: string) => {
    const consulta = valor.trim()

    if (!consulta) {
      setResultados([])
      setBuscado('')
      setError('')
      return
    }

    setCargando(true)
    setError('')

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/buscar?termino=${encodeURIComponent(consulta)}`,
      )

      if (!response.ok) {
        throw new Error('La búsqueda falló')
      }

      const data = (await response.json()) as BusquedaResponse
      setResultados(data.resultados)
      setBuscado(consulta)
    } catch {
      setError('Ocurrio un error al realizar la busqueda.')
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
