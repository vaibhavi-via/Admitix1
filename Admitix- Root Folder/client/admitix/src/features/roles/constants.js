export const ROLES_MODULE = {
  title: 'Roles',
  endpoint: '/roles',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const rolesFields = [
  { name: "role_name", label: "Role Name", type: "text", required: true },
  { name: "description", label: "Description", type: "textarea" }
]
