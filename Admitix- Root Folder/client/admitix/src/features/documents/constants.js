export const DOCUMENTS_MODULE = {
  title: 'Documents',
  endpoint: '/documents',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const documentsFields = [
  { name: "application_id", label: "Application", type: "select", required: true , format: "uuid", relation: "application" },
  { name: "document_type_id", label: "Document Type", type: "select", required: true , format: "uuid", relation: "documentType" },
  { name: "file_name", label: "File Name", type: "text", required: true },
  { name: "file_url", label: "File URL", type: "text", required: true },
  { name: "verification_status", label: "Verification Status", type: "select", options: ["pending", "verified", "rejected", "reupload_requested"] },
  { name: "verified_by", label: "Verified By", type: "select", relation: "user" },
  { name: "remarks", label: "Remarks", type: "textarea" }
]
