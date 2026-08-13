export const APPLICATION_PREFERENCES_MODULE = {
  title: 'Application Preferences',
  endpoint: '/application-preferences',
}

// Field definitions shared by the List (columns), Create, Edit and
// Details pages for this module. Add/remove/reorder fields here —
// every page picks them up automatically.
export const applicationPreferencesFields = [
  { name: "application_id", label: "Application", type: "select", required: true , format: "uuid", relation: "application" },
  { name: "course_id", label: "Course", type: "select", required: true , format: "uuid", relation: "course" },
  { name: "preference_no", label: "Preference No.", type: "number", required: true },
  { name: "status", label: "Status", type: "select", options: ["pending", "allotted", "rejected", "withdrawn"] }
]
