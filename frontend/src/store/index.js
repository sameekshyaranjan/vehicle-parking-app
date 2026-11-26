import { createPinia } from 'pinia'
import { markRaw } from 'vue'
import router from '../router'
const pinia = createPinia()
pinia.use(({ store }) => {
  store.router = markRaw(router)
})
pinia.use(({ store }) => {
  store.$onError = (error, storeId, actionName) => {
    console.error(`Error in store "${storeId}" during action "${actionName}":`, error)
    if (error.message.includes('401') || error.message.includes('Unauthorized')) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      router.push('/login')
    }
    if (typeof window !== 'undefined' && window.showError) {
      window.showError(error.message || 'An unexpected error occurred')
    }
  }
  store.$loading = false
  store.$theme = {
    primary: '#000133',
    secondary: '#4B006E',
    textAccent: '#8AB8FE',
    gradientPrimary: 'linear-gradient(135deg, #000133, #4B006E)',
    gradientSecondary: 'linear-gradient(135deg, #4B006E, #8AB8FE)'
  }
})
export default pinia
export { useAuthStore } from './modules/auth'
export { useAdminStore } from './modules/admin'
export { useParkingStore } from './modules/parking'
export { useUserStore } from './modules/user'