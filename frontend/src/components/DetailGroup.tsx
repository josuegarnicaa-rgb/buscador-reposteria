interface Props {
  title: string
  items: string[]
}
export const DetailGroup = ({ title, items }: Props) => (
  <div className="rounded-2xl border border-stone-100 bg-stone-50/60 px-4 py-3">
    <p className="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-stone-400">{title}</p>
    <ul className="flex flex-wrap gap-1.5">
      {items.map((item) => (
        <li
          key={item}
          className="rounded-full border border-amber-200/50 bg-amber-50 px-3 py-1 text-xs font-medium text-amber-900"
        >
          {item}
        </li>
      ))}
    </ul>
  </div>
)
