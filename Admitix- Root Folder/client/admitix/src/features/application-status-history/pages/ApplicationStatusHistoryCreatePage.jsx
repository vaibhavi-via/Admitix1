import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import { createApplicationStatusHistory } from '../services'
import { applicationStatusHistoryFields } from '../constants'

export default function ApplicationStatusHistoryCreatePage() {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    createApplicationStatusHistory(values)
      .then(() => navigate('/application-status-history'))
      .catch((err) => setError(err.message || 'Failed to create record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Status History Entry" subtitle="Create a new status history entry record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <EntityForm
          mode="create"
          fields={applicationStatusHistoryFields}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/application-status-history')}
          isSubmitting={isSubmitting}
          submitLabel="Create"
          error={error}
        />
      </div>
    </div>
  )
}
