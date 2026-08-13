export const SEAT_MATRIX_MODULE = {
  title: 'Seat Matrix',
  endpoint: '/seat-matrix',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const seatMatrixFields = [
  { name: "course_id", label: "Course", type: "select", required: true , format: "uuid", relation: "course" },
  { name: "category", label: "Category", type: "text", required: true },
  { name: "total_seats", label: "Total Seats", type: "number", required: true },
  { name: "filled_seats", label: "Filled Seats", type: "number", helpText: "Kept in sync automatically as application preferences are allotted." }
]
