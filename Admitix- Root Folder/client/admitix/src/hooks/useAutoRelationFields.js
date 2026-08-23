import { useEffect, useMemo, useRef, useState } from 'react'
import { FIELD_RELATIONS, loadRelationOptions } from '../components/crud/relationOptions'

// Turns any field whose `name` is a known foreign key (see
// FIELD_RELATIONS in relationOptions.js) from a raw-UUID text input
// into a searchable dropdown populated with human-readable labels —
// without every feature page having to hand-wire its own fetches.
//
// A field is left untouched (no relation lookup happens) when the
// page already gave it a non-empty `options` array or an explicit
// `type: 'select'` — that covers pages like Departments/Faculties
// that already do their own bespoke, filtered dropdown wiring.
export default function useAutoRelationFields(fields) {
  const [optionsByRelation, setOptionsByRelation] = useState({})
  const [loadingRelations, setLoadingRelations] = useState({})
  const requested = useRef(new Set())

  const relationsNeeded = useMemo(() => {
    const set = new Set()
    for (const field of fields || []) {
      const relation = FIELD_RELATIONS[field.name]
      const hasOwnOptions = Array.isArray(field.options) && field.options.length > 0
      const alreadySelect = field.type === 'select' && hasOwnOptions
      if (relation && !alreadySelect && !field.skipAutoRelation) {
        set.add(relation)
      }
    }
    return Array.from(set)
  }, [fields])

  useEffect(() => {
    relationsNeeded.forEach((relation) => {
      if (requested.current.has(relation)) return
      requested.current.add(relation)

      setLoadingRelations((prev) => ({ ...prev, [relation]: true }))

      loadRelationOptions(relation)
        .then((options) => {
          setOptionsByRelation((prev) => ({ ...prev, [relation]: options }))
        })
        .catch(() => {
          // Leave it as a plain field on failure — the raw UUID input
          // still works as a fallback, it just won't be a dropdown.
          setOptionsByRelation((prev) => ({ ...prev, [relation]: null }))
        })
        .finally(() => {
          setLoadingRelations((prev) => ({ ...prev, [relation]: false }))
        })
    })
  }, [relationsNeeded])

  const resolvedFields = useMemo(() => {
    return (fields || []).map((field) => {
      const relation = FIELD_RELATIONS[field.name]
      const hasOwnOptions = Array.isArray(field.options) && field.options.length > 0
      const alreadySelect = field.type === 'select' && hasOwnOptions

      if (!relation || alreadySelect || field.skipAutoRelation) {
        return field
      }

      const options = optionsByRelation[relation]

      // Options failed to load (or relation unknown) — fall back to
      // the original field definition rather than showing an empty,
      // unusable dropdown.
      if (options === null) {
        return field
      }

      return {
        ...field,
        type: 'select',
        format: undefined,
        loading: !!loadingRelations[relation],
        options: options || [],
      }
    })
  }, [fields, optionsByRelation, loadingRelations])

  const isLoading = relationsNeeded.some((relation) => loadingRelations[relation])

  return { fields: resolvedFields, isLoading }
}
