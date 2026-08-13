import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { createFaculty } from '../services'
import { facultiesFields } from '../constants'
import { getInstitutionsList } from '../../institutions/services'

export default function FacultyCreatePage() {
  const navigate = useNavigate()
  const [institutions, setInstitutions] = useState([])
  const [isLoadingOptions, setIsLoadingOptions] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    getInstitutionsList()
      .then((data) => setInstitutions(Array.isArray(data) ? data : data.items || []))
      .catch((err) => setError(err.message || 'Failed to load institutions.'))
      .finally(() => setIsLoadingOptions(false))
  }, [])

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
    createFaculty(values)
      .then(() => navigate('/faculties'))
      .catch((err) => setError(err.message || 'Failed to create faculty.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Faculty" subtitle="Create a new faculty record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoadingOptions && <LoadingSpinner label="Loading institutions…" />}
        {!isLoadingOptions && (
          <EntityForm
            mode="create"
            fields={fields}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/faculties')}
            isSubmitting={isSubmitting}
            submitLabel="Create"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
