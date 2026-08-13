import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { createDepartment } from '../services'
import { departmentsFields } from '../constants'
import { getInstitutionsList } from '../../institutions/services'
import { getFacultiesList } from '../../faculties/services'
import { getStaffList } from '../../staff/services'

export default function DepartmentCreatePage() {
  const navigate = useNavigate()
  const [institutions, setInstitutions] = useState([])
  const [faculties, setFaculties] = useState([])
  const [staff, setStaff] = useState([])
  const [formValues, setFormValues] = useState({ institution_id: '', faculty_id: '' })
  const [isLoadingOptions, setIsLoadingOptions] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getInstitutionsList(), getFacultiesList(), getStaffList()])
      .then(([institutionData, facultyData, staffData]) => {
        setInstitutions(Array.isArray(institutionData) ? institutionData : institutionData.items || [])
        setFaculties(Array.isArray(facultyData) ? facultyData : facultyData.items || [])
        setStaff(Array.isArray(staffData) ? staffData : staffData.items || [])
      })
      .catch((err) => setError(err.message || 'Failed to load department options.'))
      .finally(() => setIsLoadingOptions(false))
  }, [])

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
    createDepartment(values)
      .then(() => navigate('/departments'))
      .catch((err) => setError(err.message || 'Failed to create department.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Department" subtitle="Create a new department record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoadingOptions && <LoadingSpinner label="Loading department options…" />}
        {!isLoadingOptions && (
          <EntityForm
            mode="create"
            fields={fields}
            onValuesChange={handleValuesChange}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/departments')}
            isSubmitting={isSubmitting}
            submitLabel="Create"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
