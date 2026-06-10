interface Props {
  title: string
  data: Record<string, string[]>
}

export const MapGroup = ({ title, data }: Props) => (
  <div className="rounded-2xl border border-stone-100 bg-stone-50/60 px-4 py-3">
    <p className="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-stone-400">{title}</p>
    <div className="space-y-2">
      {Object.entries(data).map(([key, values]) => (
        <div key={key} className="flex flex-wrap items-baseline gap-2">
          <span className="rounded-lg bg-white/80 px-2.5 py-1 text-xs font-semibold text-stone-700 shadow-sm ring-1 ring-stone-200/60">
            {key}
          </span>
          <span className="text-xs text-stone-500">{values.join(', ')}</span>
        </div>
      ))}
    </div>
  </div>
)
