import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getDepartmentsById, updateDepartment } from '../services'
import { departmentsFields } from '../constants'
import { getInstitutionsList } from '../../institutions/services'
import { getFacultiesList } from '../../faculties/services'
import { getStaffList } from '../../staff/services'

export default function DepartmentEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [institutions, setInstitutions] = useState([])
  const [faculties, setFaculties] = useState([])
  const [staff, setStaff] = useState([])
  const [formValues, setFormValues] = useState({ institution_id: '', faculty_id: '' })
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getDepartmentsById(id), getInstitutionsList(), getFacultiesList(), getStaffList()])
      .then(([department, institutionData, facultyData, staffData]) => {
        setRecord(department)
        setFormValues({
          institution_id: department.institution_id || '',
          faculty_id: department.faculty_id || '',
        })
        setInstitutions(Array.isArray(institutionData) ? institutionData : institutionData.items || [])
        setFaculties(Array.isArray(facultyData) ? facultyData : facultyData.items || [])
        setStaff(Array.isArray(staffData) ? staffData : staffData.items || [])
      })
      .catch((err) => setError(err.message || 'Failed to load department.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const filteredFaculties = faculties.filter((faculty) =>
    !formValues.institution_id || faculty.institution_id === formValues.institution_id || faculty.id === formValues.faculty_id,
  )
  const filteredStaff = staff.filter((person) =>
    !formValues.institution_id || person.institution_id === formValues.institution_id,
  )

  const fields = useMemo(() => departmentsFields.map((field) => {
    if (field.name === 'institution_id') {
      return {
        ...field,
        options: institutions.map((item) => ({
          value: item.institution_id || item.id,
          label: `${item.institution_name}${item.institution_code ? ` (${item.institution_code})` : ''}`,
        })),
      }
    }
    if (field.name === 'faculty_id') {
      return {
        ...field,
        options: filteredFaculties.map((item) => ({
          value: item.faculty_id || item.id,
          label: item.faculty_name,
        })),
        disabled: !formValues.institution_id,
      }
    }
    if (field.name === 'hod_staff_id') {
      return {
        ...field,
        options: filteredStaff.map((item) => ({
          value: item.staff_id || item.id,
          label: `${item.employee_id}${item.designation ? ` — ${item.designation}` : ''}`,
        })),
        disabled: !formValues.institution_id,
      }
    }
    return field
  }), [institutions, filteredFaculties, filteredStaff, formValues.institution_id])

  const handleValuesChange = (next, name) => {
    if (name === 'institution_id') {
      const selectedFaculty = faculties.find((item) => (item.faculty_id || item.id) === next.faculty_id)
      if (selectedFaculty && selectedFaculty.institution_id !== next.institution_id) {
        next = { ...next, faculty_id: '', hod_staff_id: '' }
      }
    }
    setFormValues(next)
  }

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    updateDepartment(id, values)
      .then(() => navigate('/departments'))
      .catch((err) => setError(err.message || 'Failed to update department.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Edit Department" subtitle="Update this department record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <EntityForm
            mode="edit"
            fields={fields}
            initialValues={record}
            onValuesChange={handleValuesChange}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/departments')}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
