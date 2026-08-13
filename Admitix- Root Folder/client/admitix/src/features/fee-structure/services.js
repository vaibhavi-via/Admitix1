import api from '../../api/axios'

// All Fee Structure API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/fee-structure'

export function getFeeStructureList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getFeeStructureById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createFeeStructure(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateFeeStructure(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteFeeStructure(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
