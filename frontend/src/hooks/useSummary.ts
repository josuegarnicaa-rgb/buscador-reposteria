import { useEffect, useState } from 'react'
import type { Idioma, Resumen } from '../types'
import { API_BASE_URL } from '../config'
import { obtenerTextos } from '../i18n'

const resumenInicial: Resumen = {
  clases: 0,
  propiedades_objeto: 0,
  propiedades_datos: 0,
  individuos: 0,
}
export const useSummary = (idioma: Idioma) => {
  const [resumen, setResumen] = useState<Resumen>(resumenInicial)
  const [error, setError] = useState<string>('')

  useEffect(() => {
    const controller = new AbortController()

    fetch(`${API_BASE_URL}/api/resumen`, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) {
          throw new Error('No se pudo cargar el resumen')
        }

        return response.json() as Promise<Resumen>
      })
      .then((data) => setResumen(data))
      .catch((fetchError) => {
        if (fetchError instanceof DOMException && fetchError.name === 'AbortError') {
          return
        }

        setError(obtenerTextos(idioma).errorResumen)
      })

    return () => controller.abort()
  }, [])
  return {
    resumen,
    error
  }
}
