import api from '../../api/axios'

// All Roles API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/roles'

export function getRolesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getRolesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createRole(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateRole(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteRole(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
