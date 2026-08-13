import { useEffect, useMemo, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getFacultiesById, updateFaculty } from '../services'
import { facultiesFields } from '../constants'
import { getInstitutionsList } from '../../institutions/services'

export default function FacultyEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [institutions, setInstitutions] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [isLoadingOptions, setIsLoadingOptions] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([getFacultiesById(id), getInstitutionsList()])
      .then(([faculty, data]) => {
        setRecord(faculty)
        setInstitutions(Array.isArray(data) ? data : data.items || [])
      })
      .catch((err) => setError(err.message || 'Failed to load faculty.'))
      .finally(() => {
        setIsLoading(false)
        setIsLoadingOptions(false)
      })
  }, [id])

  const fields = useMemo(() => facultiesFields.map((field) =>
    field.name === 'institution_id'
      ? {
          ...field,
          options: institutions.map((item) => ({
            value: item.institution_id || item.id,
            label: `${item.institution_name}${item.institution_code ? ` (${item.institution_code})` : ''}`,
          })),
          loading: isLoadingOptions,
          disabled: isLoadingOptions,
        }
      : field,
  ), [institutions, isLoadingOptions])

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    updateFaculty(id, values)
      .then(() => navigate('/faculties'))
      .catch((err) => setError(err.message || 'Failed to update faculty.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Edit Faculty" subtitle="Update this faculty record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <EntityForm
            mode="edit"
            fields={fields}
            initialValues={record}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/faculties')}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
