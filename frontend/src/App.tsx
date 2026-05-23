import { useState } from 'react'
import type { SubmitEvent } from 'react'
import { MapGroup, DetailGroup, ResumenCard, NavBar } from './components'
import { useSearch } from './hooks/useSearch'
import { useSummary } from './hooks/useSummary'

function App() {
  const [termino, setTermino] = useState('')
  const { resumen, error: errorSummary } = useSummary()
  const { buscar, resultados, buscado, cargando, error } = useSearch()

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
                    {resultados.length} coincidencia{resultados.length === 1 ? '' : 's'} encontrada{resultados.length === 1 ? '' : 's'}
                  </p>
                </div>
              </div>
            ) : null}

            {buscado && resultados.length === 0 && !cargando ? (
              <div className="rounded-[1.75rem] border border-stone-200 bg-white px-5 py-6 text-stone-600">
                No se encontraron resultados.
              </div>
            ) : null}

            <div className="grid gap-5 lg:grid-cols-2">
              {resultados.map((resultado) => (
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
                      {resultado.fuente ? (
                        <span className="rounded-full bg-stone-100 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.18em] text-stone-700">
                          {resultado.fuente}
                        </span>
                      ) : null}
                    </div>
                  </div>

                  {resultado.imagen ? (
                    <img
                      src={resultado.imagen}
                      alt={resultado.nombre}
                      className="mt-4 h-48 w-full rounded-2xl object-cover"
                    />
                  ) : null}

                  {resultado.descripcion ? (
                    <p className="mt-4 text-sm leading-6 text-stone-600">{resultado.descripcion}</p>
                  ) : null}

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
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
