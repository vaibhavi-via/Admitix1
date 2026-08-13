import api from '../../api/axios'

// All Document Types API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/document-types'

export function getDocumentTypesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getDocumentTypesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createDocumentType(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateDocumentType(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteDocumentType(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
