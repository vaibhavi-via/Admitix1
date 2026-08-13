import api from '../../api/axios'

// All Faculties API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/faculties'

export function getFacultiesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getFacultiesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createFaculty(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateFaculty(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteFaculty(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
