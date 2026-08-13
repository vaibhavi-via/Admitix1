import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { RefreshCw } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import { getAuditLogsList } from '../services'
import { auditLogsFields } from '../constants'

export default function AuditLogsListPage() {
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const load = () => { setIsLoading(true); setError(''); getAuditLogsList().then((data) => setRows(Array.isArray(data) ? data : data.items || [])).catch((err) => setError(err.message || 'Failed to load audit logs.')).finally(() => setIsLoading(false)) }
  useEffect(load, [])
  const columns = [{ key: 'id', label: 'ID' }, ...auditLogsFields.filter((f) => f.type !== 'textarea' && f.type !== 'password').slice(0, 6).map((f) => ({ key: f.name, label: f.label }))]
  return <div><PageHeader title="Audit Logs" subtitle="Read-only audit trail of system activity." actions={<button onClick={load} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><RefreshCw size={16} />Refresh</button>} /><DataTable columns={columns} rows={rows} isLoading={isLoading} error={error} rowKey="id" onView={(row) => navigate(`/audit-logs/${row.id}`)} emptyMessage="No audit logs found yet." /></div>
}
