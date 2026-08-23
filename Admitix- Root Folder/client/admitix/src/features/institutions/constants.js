export const INSTITUTIONS_MODULE = {
  title: 'Institutions',
  endpoint: '/institutions',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const institutionsFields = [
  { name: "institution_name", label: "Institution Name", type: "text", required: true },
  { name: "institution_code", label: "Institution Code", type: "text", required: true },
  { name: "domain_id", label: "Domain", type: "select", placeholder: "Select domain (Engineering, Medical, Law, Pharmacy...)" },
  { name: "email", label: "Email", type: "email", required: true },
  { name: "phone", label: "Phone", type: "text" },
  { name: "address", label: "Address", type: "textarea" },
  { name: "city", label: "City", type: "text" },
  { name: "state", label: "State", type: "text" },
  { name: "country", label: "Country", type: "text", placeholder: "India" },
  { name: "logo_url", label: "Logo URL", type: "text" },
  { name: "status", label: "Active", type: "checkbox" }
]
