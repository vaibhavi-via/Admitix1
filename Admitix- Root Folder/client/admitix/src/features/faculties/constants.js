export const FACULTIES_MODULE = {
  title: 'Faculties',
  endpoint: '/faculties',
}

export const facultiesFields = [
  {
    name: 'institution_id',
    label: 'Institution',
    type: 'select',
    required: true,
    options: [],
    placeholder: 'Select institution',
  },
  { name: 'faculty_name', label: 'Faculty Name', type: 'text', required: true },
  { name: 'description', label: 'Description', type: 'textarea' },
  { name: 'status', label: 'Active', type: 'checkbox' },
]
