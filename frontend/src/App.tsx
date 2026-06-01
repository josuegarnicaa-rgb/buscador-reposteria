import { useState } from 'react'
import type { SubmitEvent } from 'react'
import { MapGroup, DetailGroup, ResumenCard, NavBar } from './components'
import { useSearch } from './hooks/useSearch'
import { useSummary } from './hooks/useSummary'
import { idiomasDisponibles, obtenerTextos } from './i18n'
import type { Idioma } from './types'

function App() {
  const [termino, setTermino] = useState('')
  const [idioma, setIdioma] = useState<Idioma>('es')
  const textos = obtenerTextos(idioma)
  const { resumen, error: errorSummary } = useSummary(idioma)
  const { buscar, resultados: data, buscado, cargando, error } = useSearch(idioma)

  const manejarSubmit = (evento: SubmitEvent<HTMLFormElement>) => {
    evento.preventDefault()
    void buscar(termino)
  }

  const manejarCambioIdioma = (nuevoIdioma: Idioma) => {
    setIdioma(nuevoIdioma)

    if (buscado) {
      void buscar(buscado, nuevoIdioma)
    }
  }

  return (
    <div className="min-h-screen bg-amber-50 text-stone-900">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">

        <NavBar badge={textos.navBadge} title={textos.navTitle} />

        <main className="flex-1 py-8 sm:py-10">
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <ResumenCard label={textos.summaryClases} value={resumen.clases} accent="from-amber-200 to-orange-100" />
            <ResumenCard label={textos.summaryObjectProperties} value={resumen.propiedades_objeto} accent="from-rose-200 to-orange-100" />
            <ResumenCard label={textos.summaryDataProperties} value={resumen.propiedades_datos} accent="from-yellow-100 to-amber-50" />
            <ResumenCard label={textos.summaryIndividuos} value={resumen.individuos} accent="from-orange-200 to-amber-100" />
          </section>

          <section className="mt-6 rounded-4xl bg-white/85 p-4 backdrop-blur sm:p-3">
            <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-stone-400">
                  {textos.languageLabel}
                </p>
                <p className="mt-1 text-sm text-stone-500">{textos.languageHelp}</p>
              </div>

              <label className="flex items-center gap-3 rounded-2xl border border-stone-200 bg-white px-4 py-3 shadow-sm">
                <span className="text-sm font-medium text-stone-700">{textos.languageLabel}</span>
                <select
                  value={idioma}
                  onChange={(event) => manejarCambioIdioma(event.target.value as Idioma)}
                  className="rounded-xl border border-stone-200 bg-stone-50 px-3 py-2 text-sm font-medium text-stone-800 outline-none transition focus:border-stone-400"
                >
                  {idiomasDisponibles.map((opcion) => (
                    <option key={opcion.value} value={opcion.value}>
                      {opcion.label}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <form onSubmit={manejarSubmit} className="flex flex-col gap-1 md:flex-row">
              <input
                type="text"
                name="termino"
                value={termino}
                onChange={(event) => setTermino(event.target.value)}
                placeholder={textos.searchPlaceholder}
                className="flex-1 rounded-2xl bg-white px-4 py-3 text-base outline-none ring-1 ring-stone-200 transition focus:ring-2 focus:ring-stone-900/10"
              />
              <button
                type="submit"
                className="rounded-2xl bg-stone-900 px-6 py-4 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-stone-800 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={cargando}
              >
                {cargando ? textos.searchingButton : textos.searchButton}
              </button>
            </form>

            {error || errorSummary ? (
              <p className="mt-4 rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-500">
                {error || errorSummary}
              </p>
            ) : null}
          </section>

          <section className="mt-8">
            {buscado ? (
              <div className="mb-4 flex items-end justify-between gap-3">
                <div>
                  <h2 className="text-2xl font-semibold tracking-tight text-stone-900">
                    {textos.resultsFor} “{buscado}”
                  </h2>
                  <p className="mt-1 text-sm text-stone-600">
                    {data?.total} {data?.total === 1 ? textos.resultsFoundSingular : textos.resultsFoundPlural}
                  </p>
                </div>
              </div>
            ) : null}

            {buscado && data?.total === 0 && !cargando ? (
              <div className="rounded-[1.75rem] border border-stone-200 bg-white px-5 py-6 text-stone-600">
                {textos.noResults}
              </div>
            ) : null}

            <div className="grid gap-5 lg:grid-cols-2">
              {data?.resultados.map((resultado) => (
                <article
                  key={resultado.id}
                  className="overflow-hidden rounded-[1.75rem] bg-white p-5 hover:-translate-y-0.5 hover:shadow-lg"
                >
                  <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                      <h3 className="text-xl font-semibold text-stone-900">{resultado.nombre}</h3>
                      <p className="mt-1 text-sm text-stone-500">{textos.elementPrefix} {resultado.tipo}</p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <span className="rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-amber-900">
                        {resultado.tipo}
                      </span>
                    </div>
                  </div>

                  <div className="mt-5 space-y-4 text-sm text-stone-700">
                    {resultado.clases.length > 0 ? (
                      <DetailGroup title={textos.classesLabel} items={resultado.clases} />
                    ) : null}
                    {resultado.superclases.length > 0 ? (
                      <DetailGroup title={textos.superclassesLabel} items={resultado.superclases} />
                    ) : null}
                    {Object.keys(resultado.relaciones).length > 0 ? (
                      <MapGroup title={textos.relationsLabel} data={resultado.relaciones} />
                    ) : null}
                    {Object.keys(resultado.atributos).length > 0 ? (
                      <MapGroup title={textos.attributesLabel} data={resultado.atributos} />
                    ) : null}
                    {Object.keys(resultado.usado_en).length > 0 ? (
                      <MapGroup title={textos.usedInLabel} data={resultado.usado_en} />
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
                        {textos.noImageLabel}
                      </div>
                    )}

                    <div className="absolute inset-x-0 bottom-0 h-24 bg-linear-to-t from-stone-950/70 to-transparent" />
                    <div className="absolute bottom-4 left-4 right-4">
                      <span className="inline-flex rounded-full bg-white/90 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-stone-700 backdrop-blur">
                        DBpedia
                      </span>
                      <h3 className="mt-3 text-2xl font-semibold leading-tight text-white drop-shadow-sm">
                        {dbp.nombre}
                      </h3>
                    </div>
                  </div>

                  <div className="space-y-5 p-5">
                    {dbp.typeLabel ? (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-[0.2em] text-stone-400">
                          {textos.typeLabel}
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
                          {textos.countriesLabel}
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
                          {textos.ingredientsLabel}
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
