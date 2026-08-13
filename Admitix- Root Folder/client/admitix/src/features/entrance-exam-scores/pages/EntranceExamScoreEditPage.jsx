import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import LoadingSpinner from '../../../components/LoadingSpinner'
import { getEntranceExamScoresById, updateEntranceExamScore } from '../services'
import { entranceExamScoresFields } from '../constants'

export default function EntranceExamScoreEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [record, setRecord] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    setIsLoading(true)
    getEntranceExamScoresById(id)
      .then(setRecord)
      .catch((err) => setError(err.message || 'Failed to load record.'))
      .finally(() => setIsLoading(false))
  }, [id])

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    updateEntranceExamScore(id, values)
      .then(() => navigate('/entrance-exam-scores'))
      .catch((err) => setError(err.message || 'Failed to update record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Edit Entrance Exam Score" subtitle="Update this entrance exam score record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        {isLoading && <LoadingSpinner label="Loading record…" />}
        {!isLoading && error && !record && <p className="text-sm text-red-600">{error}</p>}
        {!isLoading && record && (
          <EntityForm
            mode="edit"
          fields={entranceExamScoresFields}
            initialValues={record}
            onSubmit={handleSubmit}
            onCancel={() => navigate('/entrance-exam-scores')}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
            error={error}
          />
        )}
      </div>
    </div>
  )
}
