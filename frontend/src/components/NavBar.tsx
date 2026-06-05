interface Props {
  badge: string
  title: string
}

export const NavBar = ({ badge, title }: Props) => (
  <header className="overflow-hidden rounded-4xl border border-white/30 bg-white/90 shadow-xl backdrop-blur-sm">
    <div className="relative px-6 py-10 sm:px-10 sm:py-14">

      {/* Glow decorativo en la esquina */}
      <div className="absolute -right-10 -top-10 h-48 w-48 rounded-full bg-amber-300/20 blur-3xl" />
      <div className="absolute -bottom-8 left-1/3 h-32 w-32 rounded-full bg-rose-300/20 blur-2xl" />

      <div className="relative max-w-3xl">
        <p className="mb-3 inline-flex rounded-full border border-amber-300/40 bg-amber-100/20 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-amber-900/90 backdrop-blur-sm">
          {badge}
        </p>
        <h1 className="max-w-2xl text-2xl font-semibold tracking-tight text-stone-900 drop-shadow-sm sm:text-3xl">
          {title}
        </h1>
      </div>
    </div>
  </header>
)
