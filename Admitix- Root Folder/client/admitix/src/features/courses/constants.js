export const COURSES_MODULE = {
  title: 'Courses',
  endpoint: '/courses',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const coursesFields = [
  { name: "department_id", label: "Department", type: "select", required: true , format: "uuid", relation: "department" },
  { name: "institution_id", label: "Institution", type: "select", required: true , format: "uuid", relation: "institution" },
  { name: "course_name", label: "Course Name", type: "text", required: true },
  { name: "course_code", label: "Course Code", type: "text", required: true },
  { name: "duration_years", label: "Duration (Years)", type: "number", required: true },
  { name: "eligibility", label: "Eligibility", type: "textarea" },
  { name: "total_seats", label: "Total Seats", type: "number", readOnly: true, helpText: "Kept in sync automatically from the Seat Matrix \u2014 edits here may be overwritten." },
  { name: "status", label: "Active", type: "checkbox" }
]
