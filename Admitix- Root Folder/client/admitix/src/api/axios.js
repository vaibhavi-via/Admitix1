import axios from 'axios'

// Every module's services.js imports THIS instance, never axios directly.
// That means auth headers, error handling, and the base URL only ever
// need to be configured in one place.
function normalizeResponseData(data) {
  if (Array.isArray(data)) {
    return data.map(normalizeResponseData)
  }
  if (data && typeof data === 'object') {
    const normalized = { ...data }
    if (normalized.id == null) {
      const idKey = Object.keys(normalized).find((key) => key.endsWith('_id'))
      if (idKey) normalized.id = normalized[idKey]
    }
    return normalized
  }
  return data
}

function normalizeApiError(error) {
  const detail = error.response?.data?.detail
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item
        const location = Array.isArray(item?.loc) ? item.loc.filter(Boolean).join(' → ') : ''
        const message = item?.msg || 'Validation error'
        return location ? `${location}: ${message}` : message
      })
      .join(' | ')
  }
  if (detail && typeof detail === 'object') {
    return detail.msg || JSON.stringify(detail)
  }
  return error.response?.data?.message || detail || error.message || 'Something went wrong. Please try again.'
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach the access token to every outgoing request, if we have one.
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Centralized response handling: normalize errors and react to 401s.
api.interceptors.response.use(
  (response) => {
    response.data = normalizeResponseData(response.data)
    return response
  },
  async (error) => {
    const status = error.response?.status

    if (status === 401) {
      const original = error.config
      const refresh = localStorage.getItem('refresh_token')
      if (refresh && !original?._retry && !original?.url?.includes('/auth/refresh-token')) {
        original._retry = true
        try {
          const r = await axios.post(`${API_BASE_URL}/auth/refresh-token`, { refresh_token: refresh })
          localStorage.setItem('access_token', r.data.access_token)
          localStorage.setItem('refresh_token', r.data.refresh_token)
          original.headers.Authorization = `Bearer ${r.data.access_token}`
          return api(original)
        } catch {}
      }
      localStorage.removeItem('access_token'); localStorage.removeItem('refresh_token'); localStorage.removeItem('user')
      if (!window.location.pathname.startsWith('/login') && !window.location.pathname.startsWith('/register')) window.location.href = '/login'
    }

    const message = normalizeApiError(error)

    return Promise.reject({ ...error, message })
  }
)

export default api
