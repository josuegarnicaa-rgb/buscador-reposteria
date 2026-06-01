import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import './App.css'
import { MapGroup, DetailGroup } from './components'
import { useSearch } from './hooks/useSearch'
import { useSummary } from './hooks/useSummary'

function App() {
  const [termino, setTermino] = useState('')
  const { resumen, error: errorSummary } = useSummary()
  const { buscar, resultados: data, buscado, cargando, error } = useSearch()

  useEffect(() => {
    const temporizador = window.setTimeout(() => {
      void buscar(termino)
    }, 500)

    return () => window.clearTimeout(temporizador)
  }, [termino, buscar])

  const manejarSubmit = (evento: FormEvent<HTMLFormElement>) => {
    evento.preventDefault()
    void buscar(termino)
  }

  const tieneDatosMapa = (mapa: Record<string, string[]>) => {
    return Object.keys(mapa).length > 0
  }

  return (
    <div className="pagina">
      <div className="decoracion decoracion1"></div>
      <div className="decoracion decoracion2"></div>
      <div className="decoracion decoracion3"></div>
      <div className="decoracion decoracion4"></div>

      <main className="contenedorPrincipal">
        <section className="hero">
          <div className="heroSplash splash1"></div>
          <div className="heroSplash splash2"></div>
          <div className="heroSplash splash3"></div>
          <div className="heroSplash splash4"></div>

          <div className="heroContenido">
            <div className="heroEtiqueta">
              REPOSTERÍA
            </div>

            <h1 className="heroTitulo">
              Consulta productos, recetas, ingredientes, herramientas y
              relaciones de la ontología.
            </h1>

            <p className="heroTexto">
              Encuentra tortas, galletas, masas, cremas y recetas relacionadas
              con tu ontología de repostería.
            </p>
          </div>
        </section>

        <section className="resumenGrid">
          <div className="tarjetaResumen amarillo">
            <div className="lineaDecorativa"></div>
            <h3>CLASES</h3>
            <p>{resumen?.clases ?? 0}</p>
          </div>

          <div className="tarjetaResumen rosado">
            <div className="lineaDecorativa"></div>
            <h3>OBJECT PROPERTIES</h3>
            <p>{resumen?.propiedades_objeto ?? 0}</p>
          </div>

          <div className="tarjetaResumen lila">
            <div className="lineaDecorativa"></div>
            <h3>DATA PROPERTIES</h3>
            <p>{resumen?.propiedades_datos ?? 0}</p>
          </div>

          <div className="tarjetaResumen durazno">
            <div className="lineaDecorativa"></div>
            <h3>INDIVIDUOS</h3>
            <p>{resumen?.individuos ?? 0}</p>
          </div>
        </section>

        <section className="buscadorCaja">
          <form className="buscadorFormulario" onSubmit={manejarSubmit}>
            <input
              type="text"
              value={termino}
              onChange={(evento) => setTermino(evento.target.value)}
              placeholder="Buscar: torta de chocolate, galletas de crema, recetaTortaChocolate..."
              className="buscadorInput"
            />

            <button type="submit" className="botonBuscar">
              Buscar
            </button>
          </form>

          {cargando && (
            <p className="mensajeInfo">Buscando resultados...</p>
          )}

          {error && (
            <p className="mensajeError">{error}</p>
          )}

          {errorSummary && (
            <p className="mensajeError">{errorSummary}</p>
          )}
        </section>

        {data && (
          <section className="resultadosSeccion">
            <div className="tituloResultados">
              <div>
                <h2>Resultados para “{buscado}”</h2>
                <span>{data.total} coincidencias encontradas</span>
              </div>

              {typeof data.tiempo_ms === 'number' && (
                <p className="tiempoBusqueda">
                  Tiempo: {data.tiempo_ms} ms
                </p>
              )}
            </div>

            {data.total === 0 ? (
              <div className="sinResultados">
                <h3>No se encontraron resultados</h3>
                <p>
                  Intenta buscar con otra palabra como torta, chocolate,
                  galletas, crema o masa.
                </p>
              </div>
            ) : (
              <div className="resultadosGrid">
                {data.resultados.map((resultado) => (
                  <article className="tarjetaResultado" key={`local-${resultado.nombre}`}>
                    <div className="resultadoCabecera">
                      <span className="resultadoOrigen">Ontología local</span>
                      <span className="resultadoTipo">{resultado.tipo}</span>
                    </div>

                    <h3 className="resultadoTitulo">{resultado.nombre}</h3>

                    {resultado.clases.length > 0 && (
                      <DetailGroup title="Clases" items={resultado.clases} />
                    )}

                    {resultado.superclases.length > 0 && (
                      <DetailGroup title="Superclases" items={resultado.superclases} />
                    )}

                    {tieneDatosMapa(resultado.atributos) && (
                      <MapGroup title="Atributos" data={resultado.atributos} />
                    )}

                    {tieneDatosMapa(resultado.relaciones) && (
                      <MapGroup title="Relaciones" data={resultado.relaciones} />
                    )}

                    {tieneDatosMapa(resultado.usado_en) && (
                      <MapGroup title="Usado en" data={resultado.usado_en} />
                    )}
                  </article>
                ))}

                {data.dbpedia.map((resultado) => (
                  <article className="tarjetaResultado" key={`dbpedia-${resultado.enlace}`}>
                    <div className="resultadoCabecera">
                      <span className="resultadoOrigen">DBpedia</span>
                      <span className="resultadoTipo">
                        {resultado.typeLabel || 'Resultado externo'}
                      </span>
                    </div>

                    <h3 className="resultadoTitulo">{resultado.nombre}</h3>

                    {resultado.imagen ? (
                      <img
                        src={resultado.imagen}
                        alt={resultado.nombre}
                        className="resultadoImagen"
                      />
                    ) : (
                      <div className="resultadoSinImagen">
                        Sin imagen disponible
                      </div>
                    )}

                    {resultado.abstract && (
                      <p className="resultadoDescripcion">
                        {resultado.abstract}
                      </p>
                    )}

                    {resultado.ingredientes.length > 0 && (
                      <DetailGroup
                        title="Ingredientes"
                        items={resultado.ingredientes}
                      />
                    )}

                    {resultado.countries.length > 0 && (
                      <DetailGroup
                        title="Categorías"
                        items={resultado.countries}
                      />
                    )}

                    {resultado.enlace && (
                      <a
                        href={resultado.enlace}
                        target="_blank"
                        rel="noreferrer"
                        className="resultadoEnlace"
                      >
                        Ver recurso
                      </a>
                    )}
                  </article>
                ))}
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  )
}

export default App