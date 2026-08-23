export const DOCUMENTS_MODULE = {
  title: 'Documents',
  endpoint: '/documents',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const documentsFields = [
  { name: "application_id", label: "Application ID", type: "text", required: true , format: "uuid" },
  { name: "document_type_id", label: "Document Type ID", type: "text", required: true , format: "uuid" },
  { name: "file_name", label: "File Name", type: "text", required: true },
  { name: "file_url", label: "File URL", type: "text", required: true },
  { name: "verification_status", label: "Verification Status", type: "select", options: ["pending", "verified", "rejected", "reupload_requested"] },
  { name: "verified_by", label: "Verified By (User ID)", type: "text" },
  { name: "remarks", label: "Remarks", type: "textarea" }
]
