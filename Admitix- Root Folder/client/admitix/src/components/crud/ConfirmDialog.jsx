 import { AlertTriangle, X } from 'lucide-react'

export default function ConfirmDialog({
  open,
  title = 'Are you sure?',
  message,
  confirmLabel = 'Delete',
  isLoading = false,
  onConfirm,
  onCancel,
}) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4 backdrop-blur-sm">
      <div className="w-full max-w-md overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-2xl">

        {/* Header */}
        <div className="flex items-start gap-4 p-6">

          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-red-50 text-red-600">
            <AlertTriangle size={22} strokeWidth={2} />
          </div>

          <div className="min-w-0 flex-1">
            <h2 className="text-lg font-bold tracking-tight text-slate-900">
              {title}
            </h2>

            {message && (
              <p className="mt-1.5 text-sm leading-6 text-slate-500">
                {message}
              </p>
            )}
          </div>

          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="rounded-xl p-2 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <X size={18} />
          </button>
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3 border-t border-slate-100 bg-slate-50/70 px-6 py-4">

          <button
            type="button"
            onClick={onCancel}
            disabled={isLoading}
            className="
              rounded-xl
              border border-slate-200
              bg-white
              px-4 py-2.5
              text-sm font-semibold text-slate-600
              shadow-sm
              transition
              hover:bg-slate-50
              hover:text-slate-800
              disabled:cursor-not-allowed
              disabled:opacity-50
            "
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={onConfirm}
            disabled={isLoading}
            className="
              rounded-xl
              bg-red-600
              px-4 py-2.5
              text-sm font-semibold text-white
              shadow-sm
              transition
              hover:bg-red-700
              hover:shadow-md
              disabled:cursor-not-allowed
              disabled:opacity-50
            "
          >
            {isLoading ? 'Deleting...' : confirmLabel}
          </button>

        </div>
      </div>
    </div>
  )
}