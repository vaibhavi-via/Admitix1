import api from '../../api/axios'

// Real backend auth calls. AuthContext.jsx currently calls api.post('/auth/login', ...)
// directly — swap those lines for these functions once you're ready to drop mock auth.
export function loginRequest(payload) {
  return api.post('/auth/login', payload).then((res) => res.data)
}

export function logoutRequest() {
  return api.post('/auth/logout').then((res) => res.data)
}

export function getCurrentUser() {
  return api.get('/auth/me').then((res) => res.data)
}
