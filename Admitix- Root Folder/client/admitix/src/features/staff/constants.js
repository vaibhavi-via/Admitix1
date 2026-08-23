export const STAFF_MODULE = {
  title: 'Staff',
  endpoint: '/staff',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const staffFields = [
  { name: "user_id", label: "User ID", type: "text", required: true , format: "uuid" },
  { name: "institution_id", label: "Institution ID", type: "text", required: true , format: "uuid" },
  { name: "department_id", label: "Department ID", type: "text" , format: "uuid" },
  { name: "employee_id", label: "Employee ID", type: "text", required: true },
  { name: "designation", label: "Designation", type: "text" },
  { name: "joining_date", label: "Joining Date", type: "date" },
  { name: "status", label: "Active", type: "checkbox" }
]
