import type { DBpedia } from "../types"

interface Props {
  noImageLabel: string
  classOrigin: string
  typeLabel: string
  countriesLabel: string
  ingredientsLabel: string
  sourceLabel: string
  sourceButton: string
  dbp: DBpedia
}

export const DBPediaCard = ({ noImageLabel, classOrigin, typeLabel, countriesLabel, ingredientsLabel, sourceLabel, sourceButton, dbp }: Props) => {
  return (<article
    key={dbp.id}
    className="overflow-hidden rounded-[1.75rem] border border-stone-200 bg-white/90 shadow-md transition hover:-translate-y-0.5 hover:shadow-xl"
  >
    <div className="relative overflow-hidden bg-linear-to-br from-amber-100 via-stone-50 to-stone-100">
      {dbp.imagen ? (
        <img
          src={dbp.imagen}
          alt={dbp.nombre}
          className="h-56 w-full object-cover"
        />
      ) : (
        <div className="flex h-56 items-center justify-center px-6 text-center text-sm font-medium tracking-wide text-stone-500">
          {noImageLabel}
        </div>
      )}

      <div className="absolute inset-x-0 bottom-0 h-24 bg-linear-to-t from-stone-950/70 to-transparent" />
      <div className="absolute bottom-4 left-4 right-4">
        <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] ${classOrigin} backdrop-blur`}>
          {dbp.origen}
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
            {typeLabel}
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
            {countriesLabel}
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
            {ingredientsLabel}
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

      <div className="flex items-center justify-between gap-3 border-t border-stone-100 pt-4">
        <span className="text-xs text-stone-500">{sourceLabel}</span>
        <a
          href={dbp.enlace}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center rounded-full bg-stone-900 px-4 py-2 text-sm font-semibold text-white transition hover:bg-stone-800"
        >
          {sourceButton}
        </a>
      </div>
    </div>
  </article>
  )
}
