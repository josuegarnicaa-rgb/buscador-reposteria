interface Props {
  label: string
  value: number
  accent: string
}

export const ResumenCard = ({ label, value, accent }: Props) => {
  return (
    <article className="rounded-[1.75rem] border border-white/70 bg-white/90 p-5">
      <div className={`h-1.5 w-16 rounded-full bg-linear-to-r ${accent}`} />
      <p className="mt-4 text-sm font-medium uppercase tracking-[0.2em] text-stone-500">{label}</p>
      <p className="mt-2 text-3xl font-semibold text-stone-900">{value}</p>
    </article>
  )
}



