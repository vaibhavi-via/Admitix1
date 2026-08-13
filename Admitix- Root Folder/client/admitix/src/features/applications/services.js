import api from '../../api/axios'

// All Applications API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/applications'

export function getApplicationsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getApplicationsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createApplication(payload) {
    const { student_id, cycle_id, remarks } = payload
  return api.post(BASE_URL, { student_id, cycle_id, remarks }).then((res) => res.data)
}

export function updateApplication(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteApplication(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
