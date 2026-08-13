import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Pencil, Trash2, ArrowLeft } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DetailField from '../../../components/crud/DetailField'
import LoadingSpinner from '../../../components/LoadingSpinner'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getFacultiesById, deleteFaculty } from '../services'
import { getInstitutionsList } from '../../institutions/services'

export default function FacultyDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [institutionName, setInstitutionName] = useState('—')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    Promise.all([getFacultiesById(id), getInstitutionsList()])
      .then(([faculty, institutionData]) => {
        const institutions = Array.isArray(institutionData) ? institutionData : institutionData.items || []
        setRecord(faculty)
        const institution = institutions.find((item) => (item.institution_id || item.id) === faculty.institution_id)
        setInstitutionName(institution?.institution_name || '—')
      })
      .catch((err) => setError(err.message || 'Failed to load faculty.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleDelete = () => {
    setIsDeleting(true)
    deleteFaculty(id)
      .then(() => navigate('/faculties'))
      .catch((err) => setError(err.message || 'Failed to delete faculty.'))
      .finally(() => { setIsDeleting(false); setConfirmOpen(false) })
  }

  return (
    <div>
      <PageHeader
        title="Faculty Details"
        subtitle="Full record detail."
        actions={
          <>
            <button onClick={() => navigate('/faculties')} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><ArrowLeft size={16} /> Back</button>
            <button onClick={() => navigate(`/faculties/${id}/edit`)} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><Pencil size={16} /> Edit</button>
            <button onClick={() => setConfirmOpen(true)} className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"><Trash2 size={16} /> Delete</button>
          </>
        }
      />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <DetailField label="Faculty Name" value={record.faculty_name} />
            <DetailField label="Institution" value={institutionName} />
            <DetailField label="Description" value={record.description} />
            <DetailField label="Active" value={record.status} />
          </dl>
        )}
      </div>
      <ConfirmDialog open={confirmOpen} title="Delete record?" message="This action cannot be undone." isLoading={isDeleting} onConfirm={handleDelete} onCancel={() => setConfirmOpen(false)} />
    </div>
  )
}
