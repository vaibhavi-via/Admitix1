export const STUDENTS_MODULE = {
  title: 'Students',
  endpoint: '/students',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const studentsFields = [
  { name: "user_id", label: "User ID", type: "text", required: true , format: "uuid" },
  { name: "institution_id", label: "Institution ID", type: "text", required: true , format: "uuid" },
  { name: "aadhaar_no", label: "Aadhaar No.", type: "text" },
  { name: "gender", label: "Gender", type: "select", options: ["male", "female", "other", "prefer_not_to_say"] },
  { name: "dob", label: "Date of Birth", type: "date" },
  { name: "blood_group", label: "Blood Group", type: "text" },
  { name: "category", label: "Category", type: "text" },
  { name: "nationality", label: "Nationality", type: "text", placeholder: "Indian" },
  { name: "address", label: "Address", type: "textarea" },
  { name: "city", label: "City", type: "text" },
  { name: "state", label: "State", type: "text" },
  { name: "pincode", label: "Pincode", type: "text" },
  { name: "parent_name", label: "Parent Name", type: "text" },
  { name: "parent_phone", label: "Parent Phone", type: "text" },
  { name: "guardian_email", label: "Guardian Email", type: "email" }
]
