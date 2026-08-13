import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getRolesById, updateRole } from '../services'
import { rolesFields } from '../constants'

export default function RoleEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setIsLoading(true)
    getRolesById(id)
      .then(setRecord)
      .catch((err) => setError(err.message || 'Failed to load record.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    updateRole(id, values)
      .then(() => navigate('/roles'))
      .catch((err) => setError(err.message || 'Failed to update record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Edit Role" subtitle="Update this role record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <EntityForm
            mode="edit"
          fields={rolesFields}
            initialValues={record}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/roles')}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
