export const ADMISSION_CYCLES_MODULE = {
  title: 'Admission Cycles',
  endpoint: '/admission-cycles',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const admissionCyclesFields = [
  { name: "institution_id", label: "Institution ID", type: "text", required: true , format: "uuid" },
  { name: "academic_year", label: "Academic Year", type: "text", required: true, placeholder: "2026-27" },
  { name: "application_start", label: "Application Start", type: "date", required: true },
  { name: "application_end", label: "Application End", type: "date", required: true },
  { name: "status", label: "Status", type: "select", options: ["upcoming", "open", "closed", "archived"] }
]
