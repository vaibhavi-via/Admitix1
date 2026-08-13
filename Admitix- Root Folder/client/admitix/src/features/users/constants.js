export const USERS_MODULE = {
  title: 'Users',
  endpoint: '/users',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const usersFields = [
  { name: "institution_id", label: "Institution", type: "select", helpText: "Leave blank for a platform-level Super Admin." , format: "uuid", relation: "institution" },
  { name: "role_id", label: "Role", type: "select", required: true , format: "uuid", relation: "role" },
  { name: "first_name", label: "First Name", type: "text", required: true },
  { name: "last_name", label: "Last Name", type: "text" },
  { name: "email", label: "Email", type: "email", required: true },
  { name: "phone", label: "Phone", type: "text" },
  { name: "password", label: "Password", type: "password", required: false, requiredOnCreate: true, placeholder: "Minimum 8 characters" },
  { name: "profile_photo", label: "Profile Photo URL", type: "text" },
  { name: "is_active", label: "Active", type: "checkbox" }
]
