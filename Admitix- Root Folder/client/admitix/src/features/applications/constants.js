export const APPLICATIONS_MODULE = {
  title: 'Applications',
  endpoint: '/applications',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const applicationsFields = [
  { name: "student_id", label: "Student ID", type: "text", required: true , format: "uuid" },
  { name: "cycle_id", label: "Admission Cycle ID", type: "text", required: true , format: "uuid" },
  { name: "application_number", label: "Application Number", type: "text", readOnly: true, helpText: "Generated automatically by the backend." },
  { name: "submission_date", label: "Submission Date", type: "date", readOnly: true },
  { name: "current_status", label: "Current Status", type: "select", options: ["draft", "submitted", "under_review", "documents_pending", "approved", "rejected", "admitted", "cancelled"] },
  { name: "assigned_staff_id", label: "Assigned Admission Officer", type: "text", format: "uuid" },
  { name: "reviewed_by", label: "Reviewed By (User ID)", type: "text" , format: "uuid" },
  { name: "remarks", label: "Remarks", type: "textarea" }
]
