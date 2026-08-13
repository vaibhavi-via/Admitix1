import { ChevronRight } from 'lucide-react'

export default function PageHeader({
  title,
  subtitle,
  actions,
}) {
  return (
    <div className="mb-7">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
        <div className="min-w-0">
          <div className="mb-2 flex items-center gap-1.5 text-xs font-medium text-slate-400">
            <span className="text-emerald-600">Admitix</span>
            <ChevronRight size={13} />
            <span className="truncate text-slate-500">
              {title}
            </span>
          </div>

          <h1 className="text-2xl font-bold tracking-tight text-slate-900 sm:text-3xl">
            {title}
          </h1>

          {subtitle && (
            <p className="mt-1.5 max-w-2xl text-sm text-slate-500">
              {subtitle}
            </p>
          )}
        </div>

        {actions && (
          <div className="flex shrink-0 flex-wrap items-center gap-2">
            {actions}
          </div>
        )}
      </div>
    </div>
  )
}