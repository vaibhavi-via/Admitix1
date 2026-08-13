import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, RefreshCw } from 'lucide-react'
import PageHeader from '../../../components/crud/PageHeader'
import DataTable from '../../../components/crud/DataTable'
import ConfirmDialog from '../../../components/crud/ConfirmDialog'
import { getDepartmentsList, deleteDepartment } from '../services'
import { getInstitutionsList } from '../../institutions/services'
import { getFacultiesList } from '../../faculties/services'

export default function DepartmentsListPage() {
  const navigate = useNavigate()
  const [rows, setRows] = useState([])
  const [institutionNames, setInstitutionNames] = useState({})
  const [facultyNames, setFacultyNames] = useState({})
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [pendingDelete, setPendingDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const load = () => {
    setIsLoading(true)
    setError('')
    Promise.all([getDepartmentsList(), getInstitutionsList(), getFacultiesList()])
      .then(([departmentData, institutionData, facultyData]) => {
        const departments = Array.isArray(departmentData) ? departmentData : departmentData.items || []
        const institutions = Array.isArray(institutionData) ? institutionData : institutionData.items || []
        const faculties = Array.isArray(facultyData) ? facultyData : facultyData.items || []
        setRows(departments)
        setInstitutionNames(Object.fromEntries(institutions.map((item) => [item.institution_id || item.id, item.institution_name])))
        setFacultyNames(Object.fromEntries(faculties.map((item) => [item.faculty_id || item.id, item.faculty_name])))
      })
      .catch((err) => setError(err.message || 'Failed to load departments.'))
      .finally(() => setIsLoading(false))
  }

  useEffect(load, [])

  const columns = [
    { key: 'department_name', label: 'Department Name' },
    { key: 'faculty_id', label: 'Faculty', render: (row) => facultyNames[row.faculty_id] || '—' },
    { key: 'institution_id', label: 'Institution', render: (row) => institutionNames[row.institution_id] || '—' },
    { key: 'hod_staff_id', label: 'HOD', render: (row) => row.hod_staff_id ? 'Assigned' : 'Not assigned' },
    { key: 'status', label: 'Active', render: (row) => row.status ? 'Yes' : 'No' },
  ]

  const handleDelete = () => {
    if (!pendingDelete) return
    setIsDeleting(true)
    deleteDepartment(pendingDelete.id)
      .then(() => { setPendingDelete(null); load() })
      .catch((err) => setError(err.message || 'Failed to delete department.'))
      .finally(() => setIsDeleting(false))
  }

  return (
    <div>
      <PageHeader
        title="Departments"
        subtitle="Manage departments records."
        actions={
          <>
            <button onClick={load} className="inline-flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50">
              <RefreshCw size={16} /> Refresh
            </button>
            <button onClick={() => navigate('/departments/new')} className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-2 text-sm font-medium text-white hover:bg-indigo-700">
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
        onView={(row) => navigate(`/departments/${row.id}`)}
        onEdit={(row) => navigate(`/departments/${row.id}/edit`)}
        onDelete={(row) => setPendingDelete(row)}
        emptyMessage="No departments found yet."
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
