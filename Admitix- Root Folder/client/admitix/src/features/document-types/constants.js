export const DOCUMENT_TYPES_MODULE = {
  title: 'Document Types',
  endpoint: '/document-types',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const documentTypesFields = [
  { name: "document_name", label: "Document Name", type: "text", required: true },
  { name: "mandatory", label: "Mandatory", type: "checkbox" },
  { name: "description", label: "Description", type: "textarea" }
]
