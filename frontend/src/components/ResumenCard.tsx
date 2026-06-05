interface Props {
  label: string
  value: number
  accent: string
}

export const ResumenCard = ({ label, value, accent }: Props) => {
  return (
    <article className={`group relative overflow-hidden rounded-[1.75rem] border border-white/40 bg-white/90 p-5 shadow-lg backdrop-blur-md transition`}>

      <div className={`absolute -right-4 -top-4 h-24 w-24 rounded-full bg-linear-to-br ${accent} opacity-60 blur-2xl transition group-hover:opacity-80`} />

      <div className="relative">
        <div className={`h-1 w-10 rounded-full bg-linear-to-r ${accent}`} />
        <p className="mt-4 text-xs font-semibold uppercase tracking-[0.2em] text-stone-700/80">{label}</p>
        <p className="mt-1 text-4xl font-bold tracking-tight text-stone-900">{value}</p>
      </div>
    </article>
  )
}
