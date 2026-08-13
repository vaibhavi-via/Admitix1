import api from '../../api/axios'

export function getReportsList() {
  return Promise.all([
    api.get('/reports/admissions'),
    api.get('/reports/payments'),
    api.get('/reports/documents'),
    api.get('/reports/students'),
  ]).then(([admissions, payments, documents, students]) => [
    ...admissions.data.map((row) => ({ report_type: 'Admissions', ...row })),
    ...payments.data.map((row) => ({ report_type: 'Payments', ...row })),
    ...documents.data.map((row) => ({ report_type: 'Documents', ...row })),
    ...students.data.map((row) => ({ report_type: 'Students', ...row })),
  ])
}
