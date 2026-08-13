import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, RefreshCw } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getFacultiesList, deleteFaculty } from '../services'
import { getInstitutionsList } from '../../institutions/services'

export default function FacultiesListPage() {
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [institutionNames, setInstitutionNames] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [pendingDelete, setPendingDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const load = () => {
    setIsLoading(true)
    setError('')
    Promise.all([getFacultiesList(), getInstitutionsList()])
      .then(([facultyData, institutionData]) => {
        const faculties = Array.isArray(facultyData) ? facultyData : facultyData.items || []
        const institutions = Array.isArray(institutionData) ? institutionData : institutionData.items || []
        setRows(faculties)
        setInstitutionNames(Object.fromEntries(
          institutions.map((item) => [item.institution_id || item.id, item.institution_name]),
        ))
      })
      .catch((err) => setError(err.message || 'Failed to load faculties.'))
      .finally(() => setIsLoading(false))
  }

  useEffect(load, [])

  const columns = [
    { key: 'faculty_name', label: 'Faculty Name' },
    { key: 'institution_id', label: 'Institution', render: (row) => institutionNames[row.institution_id] || '—' },
    { key: 'description', label: 'Description' },
    { key: 'status', label: 'Active', render: (row) => row.status ? 'Yes' : 'No' },
  ]

  const handleDelete = () => {
    if (!pendingDelete) return
    setIsDeleting(true)
    deleteFaculty(pendingDelete.id)
      .then(() => { setPendingDelete(null); load() })
      .catch((err) => setError(err.message || 'Failed to delete faculty.'))
      .finally(() => setIsDeleting(false))
  }

  return (
    <div>
      <PageHeader
        title="Faculties"
        subtitle="Manage faculties records."
        actions={
          <>
            <button onClick={load} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
              <RefreshCw size={16} /> Refresh
            </button>
            <button onClick={() => navigate('/faculties/new')} className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700">
              <Plus size={16} /> Add New
            </button>
          </>
        }
      />
      <DataTable
        columns={columns}
        rows={rows}
        isLoading={isLoading}
        error={error}
        onView={(row) => navigate(`/faculties/${row.id}`)}
        onEdit={(row) => navigate(`/faculties/${row.id}/edit`)}
        onDelete={(row) => setPendingDelete(row)}
        emptyMessage="No faculties found yet."
      />
      <ConfirmDialog
        open={!!pendingDelete}
        title="Delete record?"
        message="This action cannot be undone."
        isLoading={isDeleting}
        onConfirm={handleDelete}
        onCancel={() => setPendingDelete(null)}
      />
    </div>
  )
}
