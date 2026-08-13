export const EDUCATIONAL_DETAILS_MODULE = {
  title: 'Educational Details',
  endpoint: '/educational-details',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const educationalDetailsFields = [
  { name: "student_id", label: "Student", type: "select", required: true , format: "uuid", relation: "student" },
  { name: "qualification", label: "Qualification", type: "text", required: true },
  { name: "board_university", label: "Board / University", type: "text" },
  { name: "institution_name", label: "Institution Name", type: "text" },
  { name: "passing_year", label: "Passing Year", type: "number" },
  { name: "seat_number", label: "Seat Number", type: "text" },
  { name: "percentage", label: "Percentage", type: "number" },
  { name: "cgpa", label: "CGPA", type: "number" }
]
