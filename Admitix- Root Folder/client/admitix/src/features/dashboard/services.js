import api from '../../api/axios'

export function getDashboardStats() {
  return api.get('/dashboard/summary').then((res) => res.data)
}
