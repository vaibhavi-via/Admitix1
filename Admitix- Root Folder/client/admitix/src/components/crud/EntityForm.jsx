 import { useState } from 'react'
import { Save, X } from 'lucide-react'
import FormField from './FormField'
import { isValidUUID, normalizeUUID } from '../../utils/uuid'
import useAutoRelationFields from '../../hooks/useAutoRelationFields'

export default function EntityForm({
  fields: rawFields,
  initialValues = {},
  onSubmit,
  onCancel,
  isSubmitting = false,
  submitLabel = 'Save',
  error,
  mode = 'create',
  onValuesChange,
}) {
  // Any field whose name is a recognized foreign key (student_id,
  // course_id, reviewed_by, ...) is automatically upgraded from a
  // raw-UUID text box into a searchable dropdown of real records —
  // pages that already wire their own filtered options (Departments,
  // Faculties) are left untouched. See useAutoRelationFields.js.
  const { fields } = useAutoRelationFields(rawFields)

  const [values, setValues] = useState(() => {
    const base = {}

    rawFields.forEach((f) => {
      const incoming = initialValues[f.name]

      base[f.name] =
        incoming !== undefined && incoming !== null
          ? incoming
          : f.type === 'checkbox'
            ? false
            : ''
    })

    return base
  })

  const [fieldErrors, setFieldErrors] = useState({})

  const handleChange = (name, value) => {
    setValues((prev) => {
      const next = { ...prev, [name]: value }
      return onValuesChange?.(next, name, value) || next
    })

    setFieldErrors((prev) => ({
      ...prev,
      [name]: undefined,
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const errors = {}

    fields.forEach((f) => {
      const required =
        f.requiredOnCreate !== undefined
          ? mode === 'create'
            ? f.requiredOnCreate
            : (f.requiredOnEdit ?? f.required)
          : f.required

      const rawValue = values[f.name]

      const value =
        typeof rawValue === 'string'
          ? rawValue.trim()
          : rawValue

      if (
        required &&
        !f.readOnly &&
        (value === '' || value === null || value === undefined)
      ) {
        errors[f.name] = `${f.label} is required.`
        return
      }

      if (
        !f.readOnly &&
        f.format === 'uuid' &&
        value !== '' &&
        value !== null &&
        value !== undefined &&
        !isValidUUID(value)
      ) {
        errors[f.name] =
          `${f.label} must be a valid UUID.`
      }
    })

    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors)
      return
    }

    const normalizedValues = Object.fromEntries(
      Object.entries(values).map(([name, rawValue]) => {
        const field = fields.find((f) => f.name === name)

        const required =
          field?.requiredOnCreate !== undefined
            ? mode === 'create'
              ? field.requiredOnCreate
              : (field.requiredOnEdit ?? field.required)
            : field?.required

        const value =
          typeof rawValue === 'string'
            ? rawValue.trim()
            : rawValue

        if (
          field?.format === 'uuid' &&
          !required &&
          (value === '' ||
            value === null ||
            value === undefined)
        ) {
          return [name, null]
        }

        return [
          name,
          typeof value === 'string'
            ? normalizeUUID(value)
            : value,
        ]
      }),
    )

    onSubmit(normalizedValues)
  }

  return (
    <form onSubmit={handleSubmit}>
      {/* Server error */}
      {error && (
        <div className="mb-6 rounded-xl border border-red-200 bg-red-50 px-4 py-3">
          <div className="flex items-start gap-3">
            <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-red-100 text-xs font-bold text-red-600">
              !
            </div>

            <div>
              <p className="text-sm font-semibold text-red-800">
                Unable to save
              </p>

              <p className="mt-0.5 text-xs leading-5 text-red-600">
                {typeof error === 'string'
                  ? error
                  : JSON.stringify(error)}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Form fields */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
        <div className="border-b border-slate-100 px-5 py-4 sm:px-6">
          <h2 className="text-sm font-bold text-slate-800">
            {mode === 'edit'
              ? 'Edit information'
              : 'Record information'}
          </h2>

          <p className="mt-1 text-xs text-slate-400">
            Fields marked with <span className="text-red-500">*</span> are
            required.
          </p>
        </div>

        <div className="p-5 sm:p-6">
          <div className="grid grid-cols-1 gap-x-6 gap-y-5 md:grid-cols-2">
            {fields.map((field) => (
              <div
                key={field.name}
                className={
                  field.type === 'textarea'
                    ? 'md:col-span-2'
                    : ''
                }
              >
                <FormField
                  field={field}
                  value={values[field.name]}
                  onChange={handleChange}
                  error={fieldErrors[field.name]}
                />
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="mt-5 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-sm font-semibold text-slate-600 shadow-sm transition hover:bg-slate-50 hover:text-slate-900 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <X size={16} />
            Cancel
          </button>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="inline-flex items-center justify-center gap-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-emerald-600/20 transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <Save size={16} />

          {isSubmitting
            ? 'Saving...'
            : submitLabel}
        </button>
      </div>
    </form>
  )
}
