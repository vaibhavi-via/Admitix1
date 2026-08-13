import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Pencil, Trash2, ArrowLeft } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DetailField from '../../../components/crud/DetailField'
import LoadingSpinner from '../../../components/LoadingSpinner'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getDepartmentsById, deleteDepartment } from '../services'
import { getInstitutionsList } from '../../institutions/services'
import { getFacultiesList } from '../../faculties/services'
import { getStaffList } from '../../staff/services'

export default function DepartmentDetailsPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [institutionName, setInstitutionName] = useState('—')
  const [facultyName, setFacultyName] = useState('—')
  const [hodName, setHodName] = useState('Not assigned')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [confirmOpen, setConfirmOpen] = useState(false)
  const [isDeleting, setIsDeleting] = useState(false)

  useEffect(() => {
    Promise.all([getDepartmentsById(id), getInstitutionsList(), getFacultiesList(), getStaffList()])
      .then(([department, institutionData, facultyData, staffData]) => {
        const institutions = Array.isArray(institutionData) ? institutionData : institutionData.items || []
        const faculties = Array.isArray(facultyData) ? facultyData : facultyData.items || []
        const staff = Array.isArray(staffData) ? staffData : staffData.items || []
        setRecord(department)
        setInstitutionName(institutions.find((item) => (item.institution_id || item.id) === department.institution_id)?.institution_name || '—')
        setFacultyName(faculties.find((item) => (item.faculty_id || item.id) === department.faculty_id)?.faculty_name || '—')
        setHodName(staff.find((item) => (item.staff_id || item.id) === department.hod_staff_id)?.employee_id || 'Not assigned')
      })
      .catch((err) => setError(err.message || 'Failed to load department.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleDelete = () => {
    setIsDeleting(true)
    deleteDepartment(id)
      .then(() => navigate('/departments'))
      .catch((err) => setError(err.message || 'Failed to delete department.'))
      .finally(() => { setIsDeleting(false); setConfirmOpen(false) })
  }

  return (
    <div>
      <PageHeader
        title="Department Details"
        subtitle="Full record detail."
        actions={
          <>
            <button onClick={() => navigate('/departments')} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><ArrowLeft size={16} /> Back</button>
            <button onClick={() => navigate(`/departments/${id}/edit`)} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"><Pencil size={16} /> Edit</button>
            <button onClick={() => setConfirmOpen(true)} className="inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50"><Trash2 size={16} /> Delete</button>
          </>
        }
      />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <DetailField label="Department Name" value={record.department_name} />
            <DetailField label="Faculty" value={facultyName} />
            <DetailField label="Institution" value={institutionName} />
            <DetailField label="Head of Department" value={hodName} />
            <DetailField label="Description" value={record.description} />
            <DetailField label="Active" value={record.status} />
          </dl>
        )}
      </div>
      <ConfirmDialog open={confirmOpen} title="Delete record?" message="This action cannot be undone." isLoading={isDeleting} onConfirm={handleDelete} onCancel={() => setConfirmOpen(false)} />
    </div>
  )
}
