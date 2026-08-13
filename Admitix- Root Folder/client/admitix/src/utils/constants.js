export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  USER: 'user',
}

export const APP_NAME = 'Admitix'

// Toggle this in .env (VITE_USE_MOCK_AUTH=true) so students can build UI
// before the FastAPI backend's auth endpoints exist.
export const USE_MOCK_AUTH = import.meta.env.VITE_USE_MOCK_AUTH === 'true'
