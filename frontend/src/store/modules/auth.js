import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { API_BASE_URL } from '@/services/base-url'
const AUTH_API_URL = `${API_BASE_URL}/auth`

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const accessToken = ref(localStorage.getItem('access_token') || null)
  const refreshToken = ref(localStorage.getItem('refresh_token') || null)
  const isLoading = ref(false)
  const loginError = ref(null)
  const registrationError = ref(null)
  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => user.value?.is_admin === true)
  const userRole = computed(() => isAdmin.value ? 'admin' : 'user')
  const userName = computed(() => user.value?.fullname || user.value?.username || 'User')
  const userEmail = computed(() => user.value?.email || '')
  const requestLogin = async (endpoint, options) => {
    isLoading.value = true
    loginError.value = null
    try {
      const response = await fetch(`${AUTH_API_URL}${endpoint}`, {
        method: 'POST',
        ...options
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Login failed')
      }
      accessToken.value = data.data.tokens.access_token
      refreshToken.value = data.data.tokens.refresh_token
      user.value = data.data.user
      localStorage.setItem('access_token', accessToken.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true, user: user.value }
    } catch (error) {
      loginError.value = error.message
      throw error
    } finally {
      isLoading.value = false
    }
  }
  const login = (credentials, isAdminLogin = false) => requestLogin(
    isAdminLogin ? '/admin-login' : '/login',
    {
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    }
  )
  const loginAsDemo = (role) => requestLogin(`/demo/${role}`)
  const isDemoLoginAvailable = async () => {
    try {
      const response = await fetch(`${AUTH_API_URL}/demo`)
      return response.ok && (await response.json()).enabled === true
    } catch {
      return false
    }
  }
  const register = async (userData) => {
    isLoading.value = true
    registrationError.value = null
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Registration failed')
      }
      accessToken.value = data.data.tokens.access_token
      refreshToken.value = data.data.tokens.refresh_token
      user.value = data.data.user
      localStorage.setItem('access_token', accessToken.value)
      localStorage.setItem('refresh_token', refreshToken.value)
      localStorage.setItem('user', JSON.stringify(user.value))
      return { success: true, user: user.value }
    } catch (error) {
      registrationError.value = error.message
      throw error
    } finally {
      isLoading.value = false
    }
  }
  const logout = async () => {
    isLoading.value = true
    try {
      if (accessToken.value) {
        await fetch(`${API_BASE_URL}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          }
        })
      }
    } catch (error) {
      console.error('Logout API error:', error)
    } finally {
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      isLoading.value = false
    }
  }
  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }
    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${refreshToken.value}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Token refresh failed')
      }
      accessToken.value = data.data.access_token
      localStorage.setItem('access_token', accessToken.value)
      return accessToken.value
    } catch (error) {
      await logout()
      throw error
    }
  }
  const changePassword = async (passwordData) => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/auth/change-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: JSON.stringify(passwordData)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Password change failed')
      }
      return { success: true, message: data.message }
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }
  const initializeAuth = () => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      try {
        user.value = JSON.parse(storedUser)
      } catch (error) {
        console.error('Error parsing stored user data:', error)
        localStorage.removeItem('user')
      }
    }
  }
  const clearErrors = () => {
    loginError.value = null
    registrationError.value = null
  }
  initializeAuth()
  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    loginError,
    registrationError,
    isAuthenticated,
    isAdmin,
    userRole,
    userName,
    userEmail,
    login,
    loginAsDemo,
    isDemoLoginAvailable,
    register,
    logout,
    refreshAccessToken,
    changePassword,
    initializeAuth,
    clearErrors
  }
})
