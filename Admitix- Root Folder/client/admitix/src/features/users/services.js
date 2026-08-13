import api from '../../api/axios'

// All Users API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/users'

export function getUsersList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getUsersById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createUser(payload) {
    const { institution_id, role_id, first_name, last_name, email, phone, password, profile_photo, is_active } = payload
  return api.post(BASE_URL, { institution_id: institution_id || null, role_id, first_name, last_name, email, phone, password, profile_photo, is_active }).then((res) => res.data)
}

export function updateUser(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteUser(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
