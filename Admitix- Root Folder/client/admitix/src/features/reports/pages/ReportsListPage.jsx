import { useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getReportsList } from '../services'

// Generic list page — renders whatever columns the API returns.
// Swap this for a custom table/form once the module's shape settles.
export default function ReportsListPage() {
  const [rows, setRows] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const load = () => {
    setIsLoading(true)
    setError('')
    getReportsList()
      .then((data) => setRows(Array.isArray(data) ? data : data.items || []))
      .catch((err) => setError(err.message || 'Failed to load reports.'))
      .finally(() => setIsLoading(false))
  }

  useEffect(load, [])

  const columns = rows.length > 0 ? Object.keys(rows[0]) : []

  return (
    <div>
      <div className="flex items-center justify-between mb-5">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Reports</h1>
          <p className="text-sm text-gray-500 mt-0.5">Read-only operational reports generated from application data.</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={load}
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>
      </div>

      <div className="rounded-xl border border-gray-200 bg-white overflow-hidden">
        {isLoading && (
          <div className="p-10">
            <LoadingSpinner label="Loading reports…" />
          </div>
        )}

        {!isLoading && error && (
          <p className="p-6 text-sm text-red-600">{error}</p>
        )}

        {!isLoading && !error && rows.length === 0 && (
          <p className="p-10 text-center text-sm text-gray-500">No reports found yet.</p>
        )}

        {!isLoading && !error && rows.length > 0 && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 text-sm">
              <thead className="bg-gray-50">
                <tr>
                  {columns.map((col) => (
                    <th key={col} className="px-4 py-2.5 text-left font-medium text-gray-600 whitespace-nowrap">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {rows.map((row, i) => (
                  <tr key={row.id ?? i} className="hover:bg-gray-50">
                    {columns.map((col) => (
                      <td key={col} className="px-4 py-2.5 text-gray-700 whitespace-nowrap">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}
