import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Pencil, Trash2, ArrowLeft } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DetailField from '../../../components/crud/DetailField'
import LoadingSpinner from '../../../components/LoadingSpinner'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getSeatMatrixById, deleteSeatMatrix } from '../services'
import { seatMatrixFields } from '../constants'

export default function SeatMatrixDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    getSeatMatrixById(id)
      .then(setRecord)
      .catch((err) => setError(err.message || 'Failed to load record.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleDelete = () => {
    setIsDeleting(true)
    deleteSeatMatrix(id)
      .then(() => navigate('/seat-matrix'))
      .catch((err) => setError(err.message || 'Failed to delete record.'))
      .finally(() => {
        setIsDeleting(false)
        setConfirmOpen(false)
      })
  }

  return (
    <div>
      <PageHeader
        title="Seat Matrix Entry Details"
        subtitle="Full record detail."
        actions={
          <>
            <button
              onClick={() => navigate('/seat-matrix')}
              className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <ArrowLeft size={16} />
              Back
            </button>
            <button
              onClick={() => navigate(`/seat-matrix/${id}/edit`)}
              className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              <Pencil size={16} />
              Edit
            </button>
            <button
              onClick={() => setConfirmOpen(true)}
              className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              <Trash2 size={16} />
              Delete
            </button>
          </>
        }
      />

      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <DetailField label="ID" value={record.id} />
            {seatMatrixFields.map((f) => (
              <DetailField key={f.name} label={f.label} value={record[f.name]} />
            ))}
          </dl>
        )}
      </div>

      <ConfirmDialog
        open={confirmOpen}
        title="Delete record?"
        message="This action cannot be undone."
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setConfirmOpen(false)}
      />
    </div>
  )
}
