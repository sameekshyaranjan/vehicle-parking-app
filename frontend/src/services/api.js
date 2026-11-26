import axios from 'axios'
import { useAuthStore } from '../store/modules/auth'
import router from '../router'
import { API_BASE_URL } from './base-url'
const API_TIMEOUT = 30000
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: API_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})
apiClient.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    config.metadata = { startTime: new Date() }
    if (import.meta.env.DEV) {
      console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`, {
        data: config.data,
        params: config.params
      })
    }
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)
apiClient.interceptors.response.use(
  (response) => {
    const endTime = new Date()
    const duration = endTime.getTime() - response.config.metadata.startTime.getTime()
    if (import.meta.env.DEV) {
      console.log(`✅ API Response: ${response.config.method?.toUpperCase()} ${response.config.url}`, {
        status: response.status,
        duration: `${duration}ms`,
        data: response.data
      })
    }
    return response
  },
  async (error) => {
    const originalRequest = error.config
    if (import.meta.env.DEV) {
      console.error(`❌ API Error: ${error.config?.method?.toUpperCase()} ${error.config?.url}`, {
        status: error.response?.status,
        message: error.message,
        data: error.response?.data
      })
    }
    if (error.response) {
      const { status, data } = error.response
      switch (status) {
        case 401:
          if (!originalRequest._retry) {
            originalRequest._retry = true
            try {
              const authStore = useAuthStore()
              await authStore.refreshToken()
              originalRequest.headers.Authorization = `Bearer ${authStore.token}`
              return apiClient(originalRequest)
            } catch (refreshError) {
              const authStore = useAuthStore()
              authStore.logout()
              router.push('/login')
              return Promise.reject(refreshError)
            }
          }
          break
        case 403:
          throw new ApiError('Access denied. Insufficient permissions.', status, data)
        case 404:
          throw new ApiError('Resource not found.', status, data)
        case 422:
          throw new ApiError('Validation failed.', status, data)
        case 429:
          throw new ApiError('Too many requests. Please try again later.', status, data)
        case 500:
          throw new ApiError('Internal server error. Please try again later.', status, data)
        default:
          throw new ApiError(data?.message || 'An unexpected error occurred.', status, data)
      }
    } else if (error.request) {
      throw new ApiError('Network error. Please check your connection.', 0, null)
    } else {
      throw new ApiError('Request configuration error.', 0, null)
    }
    return Promise.reject(error)
  }
)
export class ApiError extends Error {
  constructor(message, status = 0, data = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.data = data
    this.timestamp = new Date().toISOString()
  }
  get isValidationError() {
    return this.status === 422
  }
  get isAuthError() {
    return this.status === 401 || this.status === 403
  }
  get isNetworkError() {
    return this.status === 0
  }
  get isServerError() {
    return this.status >= 500
  }
}
export class BaseApiService {
  constructor(baseEndpoint = '') {
    this.baseEndpoint = baseEndpoint
    this.client = apiClient
  }
  async get(endpoint = '', params = {}, config = {}) {
    try {
      const response = await this.client.get(
        `${this.baseEndpoint}${endpoint}`,
        { params, ...config }
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async post(endpoint = '', data = {}, config = {}) {
    try {
      const response = await this.client.post(
        `${this.baseEndpoint}${endpoint}`,
        data,
        config
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async put(endpoint = '', data = {}, config = {}) {
    try {
      const response = await this.client.put(
        `${this.baseEndpoint}${endpoint}`,
        data,
        config
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async patch(endpoint = '', data = {}, config = {}) {
    try {
      const response = await this.client.patch(
        `${this.baseEndpoint}${endpoint}`,
        data,
        config
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async delete(endpoint = '', config = {}) {
    try {
      const response = await this.client.delete(
        `${this.baseEndpoint}${endpoint}`,
        config
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async upload(endpoint = '', file, additionalData = {}, onProgress = null) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      Object.keys(additionalData).forEach(key => {
        formData.append(key, additionalData[key])
      })
      const config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      if (onProgress) {
        config.onUploadProgress = (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(percentCompleted)
        }
      }
      const response = await this.client.post(
        `${this.baseEndpoint}${endpoint}`,
        formData,
        config
      )
      return this.handleResponse(response)
    } catch (error) {
      throw this.handleError(error)
    }
  }
  async download(endpoint = '', params = {}, filename = null) {
    try {
      const response = await this.client.get(
        `${this.baseEndpoint}${endpoint}`,
        {
          params,
          responseType: 'blob'
        }
      )
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      const contentDisposition = response.headers['content-disposition']
      const extractedFilename = contentDisposition?.match(/filename="(.+)"/)?.[1]
      link.download = filename || extractedFilename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      return { success: true, filename: link.download }
    } catch (error) {
      throw this.handleError(error)
    }
  }
  handleResponse(response) {
    return {
      data: response.data,
      status: response.status,
      headers: response.headers,
      success: true
    }
  }
  handleError(error) {
    if (error instanceof ApiError) {
      return error
    }
    if (error.response) {
      return new ApiError(
        error.response.data?.message || error.message,
        error.response.status,
        error.response.data
      )
    }
    return new ApiError(error.message || 'Unknown error occurred')
  }
}
export const apiUtils = {
  buildQueryString(params) {
    const searchParams = new URLSearchParams()
    Object.keys(params).forEach(key => {
      if (params[key] !== null && params[key] !== undefined) {
        searchParams.append(key, params[key])
      }
    })
    return searchParams.toString()
  },
  formatValidationErrors(errors) {
    if (!errors || typeof errors !== 'object') return []
    return Object.keys(errors).map(field => ({
      field,
      messages: Array.isArray(errors[field]) ? errors[field] : [errors[field]]
    }))
  },
  createCacheKey(endpoint, params = {}) {
    const sortedParams = Object.keys(params)
      .sort()
      .reduce((sorted, key) => {
        sorted[key] = params[key]
        return sorted
      }, {})
    return `${endpoint}:${JSON.stringify(sortedParams)}`
  },
  debounce(func, wait) {
    let timeout
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout)
        func(...args)
      }
      clearTimeout(timeout)
      timeout = setTimeout(later, wait)
    }
  }
}
export { apiClient }
export default BaseApiService
