import api from '../../api/axios'

// All Documents API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/documents'

export function getDocumentsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getDocumentsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createDocument(payload) {
    const { application_id, document_type_id, file_name, file_url, remarks } = payload
  return api.post(BASE_URL, { application_id, document_type_id, file_name, file_url, remarks }).then((res) => res.data)
}

export function updateDocument(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteDocument(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
