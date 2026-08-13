import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import { createChat } from '../services'
import { chatFields } from '../constants'

export default function ChatCreatePage() {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    createChat(values)
      .then(() => navigate('/chat'))
      .catch((err) => setError(err.message || 'Failed to create record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Chat Entry" subtitle="Create a new chat entry record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <EntityForm
          mode="create"
          fields={chatFields}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/chat')}
          isSubmitting={isSubmitting}
          submitLabel="Create"
          error={error}
        />
      </div>
    </div>
  )
}
