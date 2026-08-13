import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PageHeader from '../../../components/crud/PageHeader'
import EntityForm from '../../../components/crud/EntityForm'
import { createCourse } from '../services'
import { coursesFields } from '../constants'

export default function CourseCreatePage() {
  const navigate = useNavigate()
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = (values) => {
    setIsSubmitting(true)
    setError('')
    createCourse(values)
      .then(() => navigate('/courses'))
      .catch((err) => setError(err.message || 'Failed to create record.'))
      .finally(() => setIsSubmitting(false))
  }

  return (
    <div>
      <PageHeader title="Add Course" subtitle="Create a new course record." />
      <div className="rounded-xl border border-gray-200 bg-white p-5">
        <EntityForm
          mode="create"
          fields={coursesFields}
          onSubmit={handleSubmit}
          onCancel={() => navigate('/courses')}
          isSubmitting={isSubmitting}
          submitLabel="Create"
          error={error}
        />
      </div>
    </div>
  )
}
