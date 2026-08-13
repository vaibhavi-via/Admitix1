 import { Eye, Pencil, Trash2, MoreHorizontal, Copy } from 'lucide-react'
import { useEffect, useState } from 'react'
import { loadRelationOptions, FIELD_RELATIONS } from './relationOptions'
import LoadingSpinner from '../LoadingSpinner'

function isUUID(value) {
  return typeof value === 'string' &&
    /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(value)
}

function CellValue({ value, isFirstColumn, displayValue }) {
  const text = String(displayValue ?? value ?? '—')

  // Internal UUIDs are never displayed in the UI.
  if (isUUID(text)) {
    return <span className="text-slate-400">—</span>
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
  const [relationMaps, setRelationMaps] = useState({})

  useEffect(() => {
    let cancelled = false
    const relations = [...new Set(
      columns
        .map((column) => FIELD_RELATIONS[column.key])
        .filter(Boolean),
    )]

    if (!relations.length) {
      setRelationMaps({})
      return undefined
    }

    Promise.all(
      relations.map(async (relation) => {
        try {
          const options = await loadRelationOptions(relation)
          return [
            relation,
            Object.fromEntries(options.map((option) => [option.value, option.label])),
          ]
        } catch {
          return [relation, {}]
        }
      }),
    ).then((results) => {
      if (!cancelled) setRelationMaps(Object.fromEntries(results))
    })

    return () => {
      cancelled = true
    }
  }, [columns])

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
                {columns.filter((col) => col.key !== 'id').map((col, index) => (
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
                  {columns.filter((col) => col.key !== 'id').map((col, columnIndex) => (
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
                          displayValue={
                            FIELD_RELATIONS[col.key]
                              ? relationMaps[FIELD_RELATIONS[col.key]]?.[row[col.key]]
                              : undefined
                          }
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