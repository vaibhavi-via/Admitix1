import api from '../../api/axios'

const BASE_URL = '/application-status-history'

export function getApplicationStatusHistoryList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getApplicationStatusHistoryById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}
