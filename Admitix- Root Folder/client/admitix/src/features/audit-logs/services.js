import api from '../../api/axios'

const BASE_URL = '/audit-logs'

export function getAuditLogsList(params) {
  return api.get(BASE_URL, { params }).then((res) => res.data)
}

export function getAuditLogsById(id) {
  return api.get(`${BASE_URL}/${id}`).then((res) => res.data)
}
