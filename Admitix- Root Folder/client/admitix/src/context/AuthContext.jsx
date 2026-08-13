import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import api from '../api/axios'
import { STORAGE_KEYS, USE_MOCK_AUTH } from '../utils/constants'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const storedUser = localStorage.getItem(STORAGE_KEYS.USER)
    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)

    if (storedUser && token) {
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem(STORAGE_KEYS.USER)
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
      }
    }

    setIsLoading(false)
  }, [])

  const login = useCallback(async ({ email, password }) => {
    if (USE_MOCK_AUTH) {
      const mockUser = {
        id: 1,
        name: 'Demo Student',
        email,
      }

      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, 'mock-token')
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(mockUser))
      setUser(mockUser)

      return mockUser
    }

    const { data } = await api.post('/auth/login', {
      email,
      password,
    })

    localStorage.setItem(
      STORAGE_KEYS.ACCESS_TOKEN,
      data.access_token,
    )

    localStorage.setItem(
      STORAGE_KEYS.USER,
      JSON.stringify(data.user),
    )

    setUser(data.user)

    return data.user
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER)
    setUser(null)
  }, [])

  const value = {
    user,
    isAuthenticated: !!user,
    isLoading,
    login,
    logout,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
} 
