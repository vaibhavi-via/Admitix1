import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  Pencil,
  Trash2,
  ArrowLeft,
  Building2,
} from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DetailField from '../../../components/crud/DetailField'
import LoadingSpinner from '../../../components/LoadingSpinner'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getInstitutionsById, deleteInstitution } from '../services'
import { institutionsFields } from '../constants'

export default function InstitutionDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()

  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    setIsLoading(true)
    setError('')

    getInstitutionsById(id)
      .then(setRecord)
      .catch((err) =>
        setError(err.message || 'Failed to load record.'),
      )
      .finally(() => setIsLoading(false))
  }, [id])

  const handleDelete = () => {
    setIsDeleting(true)

    deleteInstitution(id)
      .then(() => navigate('/institutions'))
      .catch((err) =>
        setError(err.message || 'Failed to delete record.'),
      )
      .finally(() => {
        setIsDeleting(false)
        setConfirmOpen(false)
      })
  }

  return (
    <div>
      <PageHeader
        title="Institution Details"
        subtitle="View complete institution information."
        actions={
          <>
            <button
              onClick={() => navigate('/institutions')}
              className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-slate-900"
            >
              <ArrowLeft size={16} />
              Back
            </button>

            <button
              onClick={() =>
                navigate(`/institutions/${id}/edit`)
              }
              className="inline-flex items-center gap-1.5 rounded-xl bg-emerald-600 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-emerald-600/20 transition hover:bg-emerald-700"
            >
              <Pencil size={16} />
              Edit
            </button>

            <button
              onClick={() => setConfirmOpen(true)}
              className="inline-flex items-center gap-1.5 rounded-xl border border-red-200 bg-white px-4 py-2.5 text-sm font-semibold text-red-600 transition hover:bg-red-50"
            >
              <Trash2 size={16} />
              Delete
            </button>
          </>
        }
      />

      {/* Loading */}
      {isLoading && (
        <div className="flex min-h-[300px] items-center justify-center rounded-2xl border border-slate-200 bg-white shadow-sm">
          <LoadingSpinner label="Loading record..." />
        </div>
      )}

      {/* Error */}
      {!isLoading && error && !record && (
        <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
          <div className="flex items-start gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-red-100 font-bold text-red-600">
              !
            </div>

            <div>
              <p className="text-sm font-bold text-red-800">
                Unable to load institution
              </p>

              <p className="mt-1 text-sm text-red-600">
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Details */}
      {!isLoading && record && (
        <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
          {/* Card heading */}
          <div className="border-b border-slate-100 bg-slate-50/50 px-5 py-5 sm:px-6">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-emerald-50 text-emerald-600">
                <Building2 size={21} />
              </div>

              <div>
                <h2 className="text-base font-bold text-slate-900">
                  Institution Information
                </h2>

                <p className="mt-0.5 text-xs text-slate-400">
                  Details associated with this institution.
                </p>
              </div>
            </div>
          </div>

          {/* Fields */}
          <div className="p-5 sm:p-6">
            <dl className="grid grid-cols-1 gap-x-8 gap-y-0 sm:grid-cols-2 lg:grid-cols-3">
              {institutionsFields.map((f) => (
                <DetailField
                  key={f.name}
                  label={f.label}
                  value={record[f.name]}
                />
              ))}
            </dl>
          </div>
        </div>
      )}

      <ConfirmDialog
        open={confirmOpen}
        title="Delete institution?"
        message="This action cannot be undone."
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setConfirmOpen(false)}
      />
    </div>
  )
} 
