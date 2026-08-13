import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { RefreshCw } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import { getApplicationStatusHistoryList } from '../services'
import { applicationStatusHistoryFields } from '../constants'

export default function ApplicationStatusHistoryListPage() {
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const load = () => { setIsLoading(true); setError(''); getApplicationStatusHistoryList().then((data) => setRows(Array.isArray(data) ? data : data.items || [])).catch((err) => setError(err.message || 'Failed to load application status history.')).finally(() => setIsLoading(false)) }
  useEffect(load, [])
  const columns = [{ key: 'id', label: 'ID' }, ...applicationStatusHistoryFields.filter((f) => f.type !== 'textarea' && f.type !== 'password').slice(0, 6).map((f) => ({ key: f.name, label: f.label }))]
  return <div><PageHeader title="Application Status History" subtitle="Read-only history of application status changes." actions={<button onClick={load} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><RefreshCw size={16} />Refresh</button>} /><DataTable columns={columns} rows={rows} isLoading={isLoading} error={error} rowKey="id" onView={(row) => navigate(`/application-status-history/${row.id}`)} emptyMessage="No application status history found yet." /></div>
}
