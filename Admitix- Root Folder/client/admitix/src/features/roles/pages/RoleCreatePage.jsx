import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import { createRole } from '../services'
import { rolesFields } from '../constants'

export default function RoleCreatePage() {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    createRole(values)
      .then(() => navigate('/roles'))
      .catch((err) => setError(err.message || 'Failed to create record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Role" subtitle="Create a new role record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <EntityForm
          mode="create"
          fields={rolesFields}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/roles')}
          isSubmitting={isSubmitting}
          submitLabel="Create"
          error={error}
        />
      </div>
    </div>
  )
}
