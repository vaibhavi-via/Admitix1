import api from '../../api/axios'

// All Application Preferences API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/application-preferences'

export function getApplicationPreferencesList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getApplicationPreferencesById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createApplicationPreference(payload) {
  return api.post(BASE_URL, payload).then((res) => res.data)
}

export function updateApplicationPreference(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteApplicationPreference(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
