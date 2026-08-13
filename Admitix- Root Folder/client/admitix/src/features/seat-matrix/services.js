import api from '../../api/axios'

// All Seat Matrix API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/seat-matrix'

export function getSeatMatrixList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getSeatMatrixById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createSeatMatrix(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateSeatMatrix(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteSeatMatrix(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
