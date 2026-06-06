import { useState } from 'react'
import type { SubmitEvent } from 'react'
import { MapGroup, DetailGroup, ResumenCard, NavBar, DBPediaCard } from './components'
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

  const claseOrigen = (origen: string) => {
    const etiqueta = origen.toUpperCase()

    if (etiqueta.includes('DBPEDIA') && (etiqueta.includes('LOCAL') || etiqueta.includes('LOCALE'))) {
      return 'bg-amber-100 text-amber-900'
    }

    if (etiqueta.includes('DBPEDIA')) {
      return 'bg-rose-100 text-rose-900'
    }

    return 'bg-stone-900 text-white'
  }

  return (
    <div
      className="min-h-screen text-stone-900"
      style={{
        backgroundImage: 'url(/img1.jpg)',
        backgroundColor: "rgba(0,0,0,0.3)",
        backgroundBlendMode: "multiply",
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundAttachment: 'fixed',
      }}
    >
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8 backdrop-blur-[2px]">

        <NavBar badge={textos.navBadge} title={textos.navTitle} />

        <main className="flex-1 py-8 sm:py-10">
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <ResumenCard label={textos.summaryClases} value={resumen.clases} accent="from-amber-400 to-orange-300" />
            <ResumenCard label={textos.summaryObjectProperties} value={resumen.propiedades_objeto} accent="from-rose-400 to-orange-300" />
            <ResumenCard label={textos.summaryDataProperties} value={resumen.propiedades_datos} accent="from-yellow-300 to-amber-200" />
            <ResumenCard label={textos.summaryIndividuos} value={resumen.individuos} accent="from-orange-400 to-amber-300" />
          </section>

          <section className="mt-6 rounded-4xl bg-white/90 p-5 backdrop-blur-md shadow-lg sm:p-6">

            <div className="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-stone-400">
                  {textos.languageLabel}
                </p>
                <p className="mt-1 text-sm font-medium text-stone-600">{textos.languageHelp}</p>
              </div>

              <label className="flex items-center gap-3 rounded-2xl border border-amber-50/50 bg-amber-50/30 px-4 py-2.5 shadow-sm transition ">
                <span className="text-xs font-semibold uppercase tracking-widest text-stone-500">
                  {textos.languageLabel}
                </span>
                <select
                  value={idioma}
                  onChange={(event) => manejarCambioIdioma(event.target.value as Idioma)}
                  className="rounded-xl border border-amber-200/50 bg-white/80 px-3 py-1.5 text-sm font-semibold text-stone-800 outline-none transition "
                >
                  {idiomasDisponibles.map((opcion) => (
                    <option key={opcion.value} value={opcion.value}>
                      {opcion.label}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <form onSubmit={manejarSubmit} className="flex flex-col gap-2 md:flex-row">
              <div className="relative flex-1">
                <input
                  type="text"
                  name="termino"
                  value={termino}
                  onChange={(event) => setTermino(event.target.value)}
                  placeholder={textos.searchPlaceholder}
                  className="w-full rounded-2xl border border-stone-200/80 bg-white/95 px-5 py-3.5 text-base text-stone-800 outline-none placeholder:text-stone-400 transition focus:border-amber-100 focus:ring-2 focus:ring-amber-100/50"
                />
              </div>
              <button
                type="submit"
                className="rounded-2xl bg-amber-800 px-7 py-3.5 font-semibold text-white shadow-md transition hover:-translate-y-0.5 hover:bg-amber-700 hover:shadow-lg active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-60 cursor-pointer"
                disabled={cargando}
              >
                {cargando ? textos.searchingButton : textos.searchButton}
              </button>
            </form>

            {error || errorSummary ? (
              <p className="mt-4 rounded-2xl border border-rose-200/60 bg-rose-50/80 px-4 py-3 text-sm text-rose-600">
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
                  <p className="mt-1 text-sm text-bold">
                    {data?.total} {data?.total === 1 ? textos.resultsFoundSingular : textos.resultsFoundPlural}
                  </p>
                </div>
              </div>
            ) : null}

            {buscado && data?.total === 0 && !cargando ? (
              <div className="rounded-[1.75rem] border border-stone-200 bg-white/95 px-5 py-6 text-stone-600">
                {textos.noResults}
              </div>
            ) : null}


            <div className="grid gap-5 lg:grid-cols-2">
              {data?.resultados.map((resultado) => (
                <article
                  key={resultado.id}
                  className="overflow-hidden rounded-[1.75rem] bg-white/95 p-5 shadow-md hover:-translate-y-0.5 hover:shadow-xl"
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
                      <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${claseOrigen(resultado.origen)}`}>
                        {resultado.origen}
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
            </div>

            {data?.dbpedia?.length ? (
              <div className="mt-8">
                <div className="grid gap-5 lg:grid-cols-2">
                  {data.dbpedia.map((dbp) => (
                    <DBPediaCard
                      noImageLabel={textos.noImageLabel}
                      classOrigin={claseOrigen(dbp.origen)}
                      typeLabel={textos.typeLabel}
                      countriesLabel={textos.countriesLabel}
                      ingredientsLabel={textos.ingredientsLabel}
                      sourceLabel={textos.sourceLabel}
                      sourceButton={textos.sourceButton}
                      dbp={dbp}
                    />
                  ))}
                </div>
              </div>
            ) : null}
          </section>
        </main>
      </div>
    </div>
  )
}

export default App
