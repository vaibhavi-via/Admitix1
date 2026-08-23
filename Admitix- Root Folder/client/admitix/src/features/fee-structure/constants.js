export const FEE_STRUCTURE_MODULE = {
  title: 'Fee Structure',
  endpoint: '/fee-structure',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const feeStructureFields = [
  { name: "course_id", label: "Course ID", type: "text", required: true , format: "uuid" },
  { name: "category", label: "Category", type: "text", required: true },
  { name: "tuition_fee", label: "Tuition Fee", type: "number", required: true },
  { name: "admission_fee", label: "Admission Fee", type: "number" },
  { name: "other_fee", label: "Other Fee", type: "number" },
  { name: "effective_from", label: "Effective From", type: "date", required: true }
]
