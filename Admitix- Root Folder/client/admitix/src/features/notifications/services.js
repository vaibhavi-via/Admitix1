import api from '../../api/axios'

// All Notifications API calls live here. Every page/component in this
// module should import from this file — never call `api` directly.
const BASE_URL = '/notifications'

export function getNotificationsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getNotificationsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}

export function createNotification(payload) {
    const { user_id, title, message, notification_type } = payload
  return api.post(BASE_URL, { user_id, title, message, notification_type }).then((res) => res.data)
}

export function updateNotification(id, payload) {
  return api.patch(`${BASE_URL}/${id}`, payload).then((res) => res.data)
}

export function deleteNotification(id) {
  return api.delete(`${BASE_URL}/${id}`).then((res) => res.data)
}
