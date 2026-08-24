import api from '../../api/axios'

const RELATIONS = {
  institution: {
    endpoint: '/institutions',
    idKeys: ['institution_id', 'id'],
    label: (item) => item.institution_name
      ? `${item.institution_name}${item.institution_code ? ` (${item.institution_code})` : ''}`
      : (item.name || item.email || 'Institution'),
  },
  domain: {
    endpoint: '/domains',
    idKeys: ['domain_id', 'id'],
    label: (item) => item.domain_name
      ? `${item.domain_name}${item.domain_code ? ` (${item.domain_code})` : ''}`
      : (item.name || 'Domain'),
  },
  faculty: {
    endpoint: '/faculties',
    idKeys: ['faculty_id', 'id'],
    label: (item) => item.faculty_name || item.name || 'Record',
  },
  department: {
    endpoint: '/departments',
    idKeys: ['department_id', 'id'],
    label: (item) => item.department_name || item.name || 'Record',
  },
  staff: {
    endpoint: '/staff',
    idKeys: ['staff_id', 'id'],
    label: (item) => `${item.employee_id || 'Staff'}${item.designation ? ` — ${item.designation}` : ''}`,
  },
  user: {
    endpoint: '/users',
    idKeys: ['user_id', 'id'],
    label: (item) => {
      const name = [item.first_name, item.last_name].filter(Boolean).join(' ')
      return name ? `${name}${item.email ? ` — ${item.email}` : ''}` : (item.email || 'User')
    },
  },
  role: {
    endpoint: '/roles',
    idKeys: ['role_id', 'id'],
    label: (item) => item.role_name || item.name || 'Record',
  },
  student: {
    endpoint: '/students',
    idKeys: ['student_id', 'id'],
    label: (item) => {
      const name = [item.first_name, item.last_name].filter(Boolean).join(' ')
      return name
        ? `${name}${item.student_number ? ` — ${item.student_number}` : ''}`
        : (item.student_number || item.admission_number || 'Student')
    },
  },
  admissionCycle: {
    endpoint: '/admission-cycles',
    idKeys: ['cycle_id', 'id'],
    label: (item) => `${item.academic_year || item.cycle_name || item.name || 'Record'}${item.status ? ` — ${item.status}` : ''}`,
  },
  course: {
    endpoint: '/courses',
    idKeys: ['course_id', 'id'],
    label: (item) => `${item.course_name || item.name || 'Record'}${item.course_code ? ` (${item.course_code})` : ''}`,
  },
  application: {
    endpoint: '/applications',
    idKeys: ['application_id', 'id'],
    label: (item) => item.application_number || 'Application',
  },
  documentType: {
    endpoint: '/document-types',
    idKeys: ['document_type_id', 'id'],
    label: (item) => item.document_name || item.name || 'Record',
  },
  document: {
    endpoint: '/documents',
    idKeys: ['document_id', 'id'],
    label: (item) => item.file_name || item.document_name || 'Record',
  },
  fee: {
    endpoint: '/fee-structure',
    idKeys: ['fee_id', 'id'],
    label: (item) => `${item.category || 'Fee'}${item.total_fee != null ? ` — ₹${item.total_fee}` : ''}`,
  },
}


const FIELD_RELATIONS = {
  institution_id: 'institution',
  domain_id: 'domain',
  faculty_id: 'faculty',
  department_id: 'department',
  hod_staff_id: 'staff',
  user_id: 'user',
  role_id: 'role',
  student_id: 'student',
  cycle_id: 'admissionCycle',
  course_id: 'course',
  application_id: 'application',
  document_type_id: 'documentType',
  document_id: 'document',
  fee_id: 'fee',
  // Foreign keys that don't follow the `<name>_id` convention but
  // still reference `users.user_id` — reuse the `user` relation so
  // these render as searchable dropdowns too, instead of raw UUIDs.
  assigned_staff_id: 'staff',
  reviewed_by: 'user',
  verified_by: 'user',
  changed_by: 'user',
}

function getId(item, relation) {
  return relation.idKeys.map((key) => item?.[key]).find(Boolean)
}

function unwrap(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.items)) return data.items
  if (Array.isArray(data?.data)) return data.data
  if (Array.isArray(data?.results)) return data.results
  return []
}

export async function loadRelationOptions(relation) {
  const config = RELATIONS[relation]
  if (!config) throw new Error(`Unknown relation: ${relation}`)

  const response = await api.get(config.endpoint)
  return unwrap(response.data)
    .map((item) => {
      const value = getId(item, config)
      if (!value) return null
      return { value, label: config.label(item) }
    })
    .filter(Boolean)
}

export { RELATIONS, FIELD_RELATIONS }
