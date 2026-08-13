import api from '../../api/axios'

// All Departments API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/departments'

export function getDepartmentsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getDepartmentsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createDepartment(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateDepartment(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteDepartment(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
