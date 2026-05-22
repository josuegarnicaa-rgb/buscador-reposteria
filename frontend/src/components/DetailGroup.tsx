interface Props {
  title: string
  items: string[]
}
export const DetailGroup = ({ title, items }: Props) => {
  return (
    <div>
      <p className="text-sm font-semibold text-stone-900">{title}</p>
      <ul className="mt-2 flex flex-wrap gap-2">
        {items.map((item) => (
          <li key={item} className="rounded-full bg-stone-100 px-3 py-1 text-stone-700">
            {item}
          </li>
        ))}
      </ul>
    </div>
  )
}
