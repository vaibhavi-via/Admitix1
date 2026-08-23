 import { Eye, Pencil, Trash2, MoreHorizontal, Copy } from 'lucide-react'
import { useState } from 'react'
import LoadingSpinner from '../LoadingSpinner'

function CellValue({ value, isFirstColumn }) {
  const [copied, setCopied] = useState(false)

  const text = String(value ?? '—')

  // UUID / long ID
  const isLongId =
    isFirstColumn &&
    text.length > 20 &&
    /^[0-9a-f-]+$/i.test(text)

  const copyId = async () => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)

      setTimeout(() => {
        setCopied(false)
      }, 1200)
    } catch {
      // Clipboard may not be available in every browser context.
    }
  }

  if (isLongId) {
    return (
      <button
        type="button"
        onClick={copyId}
        title={copied ? 'Copied!' : 'Copy full ID'}
        className="group inline-flex max-w-[150px] items-center gap-1.5 text-left"
      >
        <span className="truncate font-mono text-xs text-slate-500 group-hover:text-emerald-600">
          {text.slice(0, 8)}...
        </span>

        <Copy
          size={13}
          className={`shrink-0 transition ${
            copied
              ? 'text-emerald-600'
              : 'text-slate-300 group-hover:text-emerald-500'
          }`}
        />
      </button>
    )
  }

  return (
    <span
      className={
        isFirstColumn
          ? 'font-medium text-slate-800'
          : 'text-slate-600'
      }
    >
      {text}
    </span>
  )
}

export default function DataTable({
  columns,
  rows,
  rowKey = 'id',
  onView,
  onEdit,
  onDelete,
  isLoading,
  error,
  emptyMessage = 'No records found yet.',
}) {
  const hasActions = Boolean(onView || onEdit || onDelete)

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white">
      {/* Loading */}
      {isLoading && (
        <div className="flex min-h-[280px] items-center justify-center">
          <LoadingSpinner label="Loading..." />
        </div>
      )}

      {/* Error */}
      {!isLoading && error && (
        <div className="flex min-h-[260px] flex-col items-center justify-center px-6 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-red-50 text-lg font-bold text-red-500">
            !
          </div>

          <p className="mt-3 text-sm font-semibold text-slate-800">
            Something went wrong
          </p>

          <p className="mt-1 max-w-md text-xs leading-5 text-red-500">
            {error}
          </p>
        </div>
      )}

      {/* Empty */}
      {!isLoading && !error && rows.length === 0 && (
        <div className="flex min-h-[280px] flex-col items-center justify-center px-6 text-center">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-50 text-emerald-600">
            <MoreHorizontal size={24} />
          </div>

          <p className="mt-4 text-sm font-semibold text-slate-800">
            No records found
          </p>

          <p className="mt-1 max-w-sm text-xs leading-5 text-slate-400">
            {emptyMessage}
          </p>
        </div>
      )}

      {/* Table */}
      {!isLoading && !error && rows.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full table-auto text-sm">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50/70">
                {columns.map((col, index) => (
                  <th
                    key={col.key}
                    className={`whitespace-nowrap px-5 py-3.5 text-left text-[11px] font-semibold uppercase tracking-wider text-slate-500 ${
                      index === 0 ? 'w-[150px]' : ''
                    }`}
                  >
                    {col.label}
                  </th>
                ))}

                {hasActions && (
                  <th className="w-[120px] whitespace-nowrap px-5 py-3.5 text-right text-[11px] font-semibold uppercase tracking-wider text-slate-500">
                    Actions
                  </th>
                )}
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100">
              {rows.map((row, rowIndex) => (
                <tr
                  key={row[rowKey] ?? rowIndex}
                  className="group transition-colors hover:bg-emerald-50/30"
                >
                  {columns.map((col, columnIndex) => (
                    <td
                      key={col.key}
                      className={`max-w-[240px] px-5 py-4 ${
                        columnIndex === 0
                          ? 'w-[150px]'
                          : ''
                      }`}
                    >
                      {col.render ? (
                        col.render(row)
                      ) : (
                        <CellValue
                          value={row[col.key]}
                          isFirstColumn={columnIndex === 0}
                        />
                      )}
                    </td>
                  ))}

                  {hasActions && (
                    <td className="px-5 py-4">
                      <div className="flex items-center justify-end gap-1">
                        {onView && (
                          <button
                            onClick={() => onView(row)}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
                            title="View"
                          >
                            <Eye size={16} strokeWidth={1.8} />
                          </button>
                        )}

                        {onEdit && (
                          <button
                            onClick={() => onEdit(row)}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-emerald-50 hover:text-emerald-600"
                            title="Edit"
                          >
                            <Pencil size={16} strokeWidth={1.8} />
                          </button>
                        )}

                        {onDelete && (
                          <button
                            onClick={() => onDelete(row)}
                            className="flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 transition hover:bg-red-50 hover:text-red-600"
                            title="Delete"
                          >
                            <Trash2 size={16} strokeWidth={1.8} />
                          </button>
                        )}
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}