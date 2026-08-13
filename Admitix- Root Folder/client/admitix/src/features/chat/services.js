import api from '../../api/axios'

// All Chat History API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/chat-history'

export function getChatList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getChatById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createChat(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateChat(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteChat(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
