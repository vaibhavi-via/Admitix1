import api from '../../api/axios'

// All Educational Details API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/educational-details'

export function getEducationalDetailsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getEducationalDetailsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createEducationalDetail(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateEducationalDetail(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteEducationalDetail(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
