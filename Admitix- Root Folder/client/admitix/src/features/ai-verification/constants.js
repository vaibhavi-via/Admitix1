export const AI_VERIFICATION_MODULE = {
  title: 'AI Verifications',
  endpoint: '/ai-verifications',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const aiVerificationFields = [
  { name: "document_id", label: "Document ID", type: "text", required: true , format: "uuid" },
  { name: "ocr_text", label: "OCR Text", type: "textarea" },
  { name: "confidence_score", label: "Confidence Score", type: "number" },
  { name: "blur_score", label: "Blur Score", type: "number" },
  { name: "missing_fields", label: "Missing Fields", type: "text" },
  { name: "name_match", label: "Name Match", type: "checkbox" },
  { name: "status", label: "Status", type: "select", options: ["pending", "passed", "failed", "manual_review"] }
]
