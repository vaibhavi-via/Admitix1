import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
// import { Pencil, Trash2, ArrowLeft } from 'lucide-react'
import { ArrowLeft } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DetailField from '../../../components/crud/DetailField'
import LoadingSpinner from '../../../components/LoadingSpinner'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'

import { getAuditLogsById } from '../services'
import { auditLogsFields } from '../constants'

export default function AuditLogDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setIsLoading(true)
    getAuditLogsById(id)
      .then(setRecord)
      .catch((err) => setError(err.message || 'Failed to load record.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleDelete = () => {
    setIsDeleting(true)
    deleteAuditLog(id)
      .then(() => navigate('/audit-logs'))
      .catch((err) => setError(err.message || 'Failed to delete record.'))
      .finally(() => {
        setIsDeleting(false)
        setConfirmOpen(false)
      })
  }

  return (
    <div>
      <PageHeader
        title="Audit Log Entry Details"
        subtitle="Full record detail."
        actions={
          <button
            onClick={() => navigate('/audit-logs')}
            className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
          >
            <ArrowLeft size={16} />
            Back
          </button>
        }
      />

      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <DetailField label="ID" value={record.id} />
            {auditLogsFields.map((f) => (
              <DetailField key={f.name} label={f.label} value={record[f.name]} />
            ))}
          </dl>
        )}
      </div>

      {/* <ConfirmDialog
        open={confirmOpen}
        title="Delete record?"
        message="This action cannot be undone."
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setConfirmOpen(false)}
      /> */}
    </div>
  )
}
