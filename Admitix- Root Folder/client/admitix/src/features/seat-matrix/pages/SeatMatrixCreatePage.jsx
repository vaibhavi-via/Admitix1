import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import { createSeatMatrix } from '../services'
import { seatMatrixFields } from '../constants'

export default function SeatMatrixCreatePage() {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    createSeatMatrix(values)
      .then(() => navigate('/seat-matrix'))
      .catch((err) => setError(err.message || 'Failed to create record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Seat Matrix Entry" subtitle="Create a new seat matrix entry record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <EntityForm
          mode="create"
          fields={seatMatrixFields}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/seat-matrix')}
          isSubmitting={isSubmitting}
          submitLabel="Create"
          error={error}
        />
      </div>
    </div>
  )
}
