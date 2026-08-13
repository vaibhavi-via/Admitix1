import api from '../../api/axios'

// All Students API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/students'

export function getStudentsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getStudentsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createStudent(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateStudent(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteStudent(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
