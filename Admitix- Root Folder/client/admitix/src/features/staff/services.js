import api from '../../api/axios'

// All Staff API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/staff'

export function getStaffList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getStaffById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createStaff(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateStaff(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteStaff(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
