import api from '../../api/axios'

// All Admission Cycles API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/admission-cycles'

export function getAdmissionCyclesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getAdmissionCyclesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createAdmissionCycle(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateAdmissionCycle(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteAdmissionCycle(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
