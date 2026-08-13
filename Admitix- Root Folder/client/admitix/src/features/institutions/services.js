import api from '../../api/axios'

// All Institutions API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/institutions'

export function getInstitutionsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getInstitutionsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createInstitution(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateInstitution(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteInstitution(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
