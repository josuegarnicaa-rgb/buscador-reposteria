import { useCallback, useRef, useState } from 'react'
import type { BusquedaResponse } from '../types'
import { API_BASE_URL } from '../config'

export const useSearch = () => {
  const [resultados, setResultados] = useState<BusquedaResponse | null>(null)
  const [buscado, setBuscado] = useState('')
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState('')

  const controllerRef = useRef<AbortController | null>(null)
  const requestIdRef = useRef(0)

  const buscar = useCallback(async (valor: string) => {
    const consulta = valor.trim()
    const requestId = requestIdRef.current + 1
    requestIdRef.current = requestId

    controllerRef.current?.abort()

    if (!consulta) {
      setResultados(null)
      setBuscado('')
      setError('')
      setCargando(false)
      return
    }

    const controller = new AbortController()
    controllerRef.current = controller

    const timeoutId = window.setTimeout(() => controller.abort(), 8000)

    setCargando(true)
    setError('')

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/buscar?termino=${encodeURIComponent(consulta)}`,
        { signal: controller.signal },
      )

      if (!response.ok) {
        throw new Error('La búsqueda falló')
      }

      const data = (await response.json()) as BusquedaResponse

      if (requestId === requestIdRef.current) {
        setResultados(data)
        setBuscado(consulta)
      }
    } catch (fetchError) {
      if (requestId !== requestIdRef.current) {
        return
      }

      if (fetchError instanceof DOMException && fetchError.name === 'AbortError') {
        setError('La búsqueda tardó demasiado. Intenta con una frase más corta.')
      } else {
        setError('Ocurrió un error al realizar la búsqueda.')
      }
    } finally {
      window.clearTimeout(timeoutId)

      if (requestId === requestIdRef.current) {
        setCargando(false)
        controllerRef.current = null
      }
    }
  }, [])

  return {
    buscar,
    resultados,
    buscado,
    cargando,
    error,
  }
}