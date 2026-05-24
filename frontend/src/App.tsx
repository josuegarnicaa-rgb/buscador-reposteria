import { useState } from 'react'
import type { SubmitEvent } from 'react'
import { MapGroup, DetailGroup, ResumenCard, NavBar } from './components'
import { useSearch } from './hooks/useSearch'
import { useSummary } from './hooks/useSummary'

function App() {
  const [termino, setTermino] = useState('')
  const { resumen, error: errorSummary } = useSummary()
  const { buscar, resultados: data, buscado, cargando, error } = useSearch()

  const manejarSubmit = (evento: SubmitEvent<HTMLFormElement>) => {
    evento.preventDefault()
    void buscar(termino)
  }

  return (
    <div className="min-h-screen bg-amber-50 text-stone-900">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">

        <NavBar />

        <main className="flex-1 py-8 sm:py-10">
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <ResumenCard label="Clases" value={resumen.clases} accent="from-amber-200 to-orange-100" />
            <ResumenCard label="Object Properties" value={resumen.propiedades_objeto} accent="from-rose-200 to-orange-100" />
            <ResumenCard label="Data Properties" value={resumen.propiedades_datos} accent="from-yellow-100 to-amber-50" />
            <ResumenCard label="Individuos" value={resumen.individuos} accent="from-orange-200 to-amber-100" />
          </section>

          <section className="mt-6 rounded-4xl bg-white/85 p-4 backdrop-blur sm:p-3">
            <form onSubmit={manejarSubmit} className="flex flex-col gap-1 md:flex-row">
              <input
                type="text"
                name="termino"
                value={termino}
                onChange={(event) => setTermino(event.target.value)}
                placeholder="Buscar: chocolate, torta, huevo, receta..."
                className="flex-1 rounded-2xl bg-white px-2 py-2 text-base outline-none ring-0 transition  "
              />
              <button
                type="submit"
                className="rounded-2xl bg-stone-900 px-6 py-4 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={cargando}
              >
                {cargando ? 'Buscando...' : 'Buscar'}
              </button>
            </form>

            {error || errorSummary ? (
              <p className="mt-4 rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-400">
                {error || errorSummary}
              </p>
            ) : null}
          </section>

          <section className="mt-8">
            {buscado ? (
              <div className="mb-4 flex items-end justify-between gap-3">
                <div>
                  <h2 className="text-2xl font-semibold tracking-tight text-stone-900">
                    Resultados para “{buscado}”
                  </h2>
                  <p className="mt-1 text-sm text-stone-600">
                    {data?.fuentes.local} coincidencia{data?.fuentes.local === 1 ? '' : 's'} encontrada{data?.fuentes.local === 1 ? '' : 's'}
                  </p>
                </div>
              </div>
            ) : null}

            {buscado && data?.fuentes.local === 0 && !cargando ? (
              <div className="rounded-[1.75rem] border border-stone-200 bg-white px-5 py-6 text-stone-600">
                No se encontraron resultados.
              </div>
            ) : null}

            <div className="grid gap-5 lg:grid-cols-2">
              {data?.resultados.map((resultado) => (
                <article
                  key={resultado.nombre}
                  className="overflow-hidden rounded-[1.75rem] bg-white p-5 hover:-translate-y-0.5"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <h3 className="text-xl font-semibold text-stone-900">{resultado.nombre}</h3>
                      <p className="mt-1 text-sm text-stone-500">Elemento {resultado.tipo}</p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-amber-900">
                        {resultado.tipo}
                      </span>
                    </div>
                  </div>

                  <div className="mt-5 space-y-4 text-sm text-stone-700">
                    {resultado.clases.length > 0 ? (
                      <DetailGroup title="Clases" items={resultado.clases} />
                    ) : null}
                    {resultado.superclases.length > 0 ? (
                      <DetailGroup title="Superclases" items={resultado.superclases} />
                    ) : null}
                    {Object.keys(resultado.relaciones).length > 0 ? (
                      <MapGroup title="Relaciones semánticas" data={resultado.relaciones} />
                    ) : null}
                    {Object.keys(resultado.atributos).length > 0 ? (
                      <MapGroup title="Atributos" data={resultado.atributos} />
                    ) : null}
                    {Object.keys(resultado.usado_en).length > 0 ? (
                      <MapGroup title="Usado en" data={resultado.usado_en} />
                    ) : null}
                  </div>
                </article>
              ))}
              {data?.dbpedia.map((dbp) => (
                <article
                  key={dbp.enlace}
                  className="overflow-hidden rounded-[1.75rem] border border-stone-200 bg-white shadow-sm transition hover:-translate-y-0.5 hover:shadow-lg"
                >
                  <div className="relative overflow-hidden bg-linear-to-br from-amber-100 via-orange-50 to-stone-100">
                    {dbp.imagen ? (
                      <img
                        src={dbp.imagen}
                        alt={dbp.nombre}
                        className="h-56 w-full object-cover"
                      />
                    ) : (
                      <div className="flex h-56 items-center justify-center px-6 text-center text-sm font-medium tracking-wide text-stone-500">
                        Sin imagen disponible para este resultado
                      </div>
                    )}

                    <div className="absolute inset-x-0 bottom-0 h-24 bg-linear-to-t from-stone-950/70 to-transparent" />
                    <div className="absolute bottom-4 left-4 right-4">
                      <h3 className="mt-3 text-2xl font-semibold leading-tight text-white drop-shadow-sm">
                        {dbp.nombre}
                      </h3>
                    </div>
                  </div>

                  <div className="space-y-5 p-5">
                    {dbp.typeLabel ? (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-stone-400">
                          Tipo
                        </p>
                        <p className="mt-1 text-sm font-medium text-stone-800">{dbp.typeLabel}</p>
                      </div>
                    ) : null}

                    {dbp.abstract ? (
                      <p className="text-sm leading-6 text-stone-600">{dbp.abstract}</p>
                    ) : null}

                    {dbp.countries.length > 0 ? (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-stone-400">
                          Países
                        </p>
                        <div className="mt-3 flex flex-wrap gap-2">
                          {dbp.countries.map((country) => (
                            <span
                              key={country}
                              className="rounded-full bg-stone-100 px-3 py-1 text-xs font-medium text-stone-700"
                            >
                              {country}
                            </span>
                          ))}
                        </div>
                      </div>
                    ) : null}

                    {dbp.ingredientes.length > 0 ? (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-stone-400">
                          Ingredientes
                        </p>
                        <div className="mt-3 flex flex-wrap gap-2">
                          {dbp.ingredientes.map((ingrediente) => (
                            <span
                              key={ingrediente}
                              className="rounded-full bg-amber-100 px-3 py-1 text-xs font-medium text-amber-900"
                            >
                              {ingrediente}
                            </span>
                          ))}
                        </div>
                      </div>
                    ) : null}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
