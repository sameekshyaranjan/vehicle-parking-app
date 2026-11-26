import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import './assets/styles/global.css'
const pinia = createPinia()
const app = createApp(App)
app.config.globalProperties.$appConfig = {
    name: 'Vehicle Parking App V2',
    version: '2.0.0',
    apiBaseUrl: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000/api',
    theme: {
        primary: '#000133',
        secondary: '#4B006E',
        textAccent: '#8AB8FE'
    }
}
app.config.errorHandler = (err, vm, info) => {
    console.error('Global error:', err)
    console.error('Vue component:', vm)
    console.error('Error info:', info)
    if (process.env.NODE_ENV === 'production') {
        console.log('Error would be sent to tracking service in production')
    }
}
app.provide('$http', {
    get: async (url, options = {}) => {
        const token = localStorage.getItem('access_token')
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        }
        try {
            const response = await fetch(`${app.config.globalProperties.$appConfig.apiBaseUrl}${url}`, {
                method: 'GET',
                headers,
                ...options
            })
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`)
            }
            return await response.json()
        } catch (error) {
            console.error('HTTP GET Error:', error)
            throw error
        }
    },
    post: async (url, data, options = {}) => {
        const token = localStorage.getItem('access_token')
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        }
        try {
            const response = await fetch(`${app.config.globalProperties.$appConfig.apiBaseUrl}${url}`, {
                method: 'POST',
                headers,
                body: JSON.stringify(data),
                ...options
            })
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`)
            }
            return await response.json()
        } catch (error) {
            console.error('HTTP POST Error:', error)
            throw error
        }
    },
    put: async (url, data, options = {}) => {
        const token = localStorage.getItem('access_token')
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        }
        try {
            const response = await fetch(`${app.config.globalProperties.$appConfig.apiBaseUrl}${url}`, {
                method: 'PUT',
                headers,
                body: JSON.stringify(data),
                ...options
            })
            return await response.json()
        } catch (error) {
            console.error('HTTP PUT Error:', error)
            throw error
        }
    },
    delete: async (url, options = {}) => {
        const token = localStorage.getItem('access_token')
        const headers = {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` }),
            ...options.headers
        }
        try {
            const response = await fetch(`${app.config.globalProperties.$appConfig.apiBaseUrl}${url}`, {
                method: 'DELETE',
                headers,
                ...options
            })
            return await response.json()
        } catch (error) {
            console.error('HTTP DELETE Error:', error)
            throw error
        }
    }
})
app.use(pinia)
app.use(router)
app.mixin({
    methods: {
        formatCurrency(amount) {
            return new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR'
            }).format(amount)
        },
        formatDate(date) {
            return new Date(date).toLocaleDateString('en-IN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
            })
        },
        formatDateTime(date) {
            return new Date(date).toLocaleString('en-IN', {
                year: 'numeric',
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            })
        },
        showSuccess(message) {
            alert(`✅ ${message}`)
        },
        showError(message) {
            alert(`❌ ${message}`)
        },
        isAdmin() {
            const user = JSON.parse(localStorage.getItem('user') || '{}')
            return user.is_admin === true
        },
        getCurrentUser() {
            return JSON.parse(localStorage.getItem('user') || '{}')
        },
        logout() {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('user')
            this.$router.push('/login')
        }
    }
})
app.mount('#app')
console.log('🚗 Vehicle Parking App V2 initialized successfully!')