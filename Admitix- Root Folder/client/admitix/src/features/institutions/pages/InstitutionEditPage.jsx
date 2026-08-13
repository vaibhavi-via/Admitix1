import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getInstitutionsById, updateInstitution } from '../services'
import { institutionsFields } from '../constants'

export default function InstitutionEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setIsLoading(true)
    getInstitutionsById(id)
      .then(setRecord)
      .catch((err) => setError(err.message || 'Failed to load record.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    updateInstitution(id, values)
      .then(() => navigate('/institutions'))
      .catch((err) => setError(err.message || 'Failed to update record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Edit Institution" subtitle="Update this institution record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <EntityForm
            mode="edit"
          fields={institutionsFields}
            initialValues={record}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/institutions')}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
