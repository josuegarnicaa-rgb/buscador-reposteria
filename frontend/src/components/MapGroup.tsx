interface Props {
  title: string
  data: Record<string, string[]>
}

export const MapGroup = ({ title, data }: Props) => {
  return (
    <div>
      <p className="text-sm font-semibold text-stone-900">{title}</p>
      <div className="mt-2 space-y-3">
        {Object.entries(data).map(([key, values]) => (
          <div key={key} className="rounded-2xl bg-stone-50 px-4 py-3">
            <p className="font-medium text-stone-900">{key}</p>
            <p className="mt-1 text-stone-700">{values.join(', ')}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
