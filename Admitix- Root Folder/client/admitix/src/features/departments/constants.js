export const DEPARTMENTS_MODULE = {
  title: 'Departments',
  endpoint: '/departments',
}

export const departmentsFields = [
  {
    name: 'institution_id',
    label: 'Institution',
    type: 'select',
    required: true,
    options: [],
    placeholder: 'Select institution',
  },
  {
    name: 'faculty_id',
    label: 'Faculty',
    type: 'select',
    required: true,
    options: [],
    placeholder: 'Select faculty',
  },
  {
    name: 'department_name',
    label: 'Department Name',
    type: 'text',
    required: true,
  },
  {
    name: 'hod_staff_id',
    label: 'Head of Department',
    type: 'select',
    options: [],
    placeholder: 'Optional — select HOD',
  },
  {
    name: 'description',
    label: 'Description',
    type: 'textarea',
  },
  {
    name: 'status',
    label: 'Active',
    type: 'checkbox',
  },
]
