<template>
  <div class="login-form-container">
    <div class="card login-card">
      <div class="card-header text-center">
        <div class="login-header">
          <div class="app-logo mb-3">
            <i class="fas fa-car"></i>
          </div>
          <h4 class="card-title mb-1">{{ isAdminLogin ? 'Admin Login' : 'Welcome Back' }}</h4>
          <p class="card-subtitle">
            {{ isAdminLogin ? 'Access administrative panel' : 'Sign in to your parking account' }}
          </p>
        </div>
      </div>
      <div class="card-body">
        <div class="login-type-toggle mb-4">
          <div class="btn-group w-100" role="group">
            <input
              type="radio"
              class="btn-check"
              id="userLogin"
              :checked="!isAdminLogin"
              @change="setLoginType(false)"
            >
            <label class="btn btn-outline-primary" for="userLogin">
              <i class="fas fa-user me-1"></i>User Login
            </label>
            <input
              type="radio"
              class="btn-check"
              id="adminLogin"
              :checked="isAdminLogin"
              @change="setLoginType(true)"
            >
            <label class="btn btn-outline-primary" for="adminLogin">
              <i class="fas fa-user-shield me-1"></i>Admin Login
            </label>
          </div>
        </div>
        <div v-if="authStore.loginError" class="alert alert-danger alert-dismissible" role="alert">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ authStore.loginError }}
          <button type="button" class="btn-close" @click="authStore.clearErrors()"></button>
        </div>
        <form @submit.prevent="handleLogin()" novalidate>
          <div class="mb-3">
            <label for="username" class="form-label">
              <i class="fas fa-user me-1"></i>Username
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.username }"
              placeholder="Enter your username"
              required
              autocomplete="username"
              :disabled="authStore.isLoading"
            >
            <div v-if="errors.username" class="invalid-feedback">
              {{ errors.username }}
            </div>
          </div>
          <div class="mb-4">
            <label for="password" class="form-label">
              <i class="fas fa-lock me-1"></i>Password
            </label>
            <div class="input-group">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                :class="{ 'is-invalid': errors.password }"
                placeholder="Enter your password"
                required
                autocomplete="current-password"
                :disabled="authStore.isLoading"
              >
              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="togglePasswordVisibility"
                :disabled="authStore.isLoading"
              >
                <i class="fas" :class="showPassword ? 'fa-eye-slash' : 'fa-eye'"></i>
              </button>
              <div v-if="errors.password" class="invalid-feedback">
                {{ errors.password }}
              </div>
            </div>
          </div>
          <div class="mb-4">
            <div class="form-check">
              <input
                id="rememberMe"
                v-model="form.rememberMe"
                type="checkbox"
                class="form-check-input"
                :disabled="authStore.isLoading"
              >
              <label for="rememberMe" class="form-check-label">
                Remember me for 30 days
              </label>
            </div>
          </div>
          <button
            type="submit"
            class="btn btn-primary w-100 mb-3"
            :disabled="authStore.isLoading || !isFormValid"
          >
            <span v-if="authStore.isLoading && !pendingDemoRole" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-sign-in-alt me-1"></i>
            {{ authStore.isLoading && !pendingDemoRole ? 'Signing In...' : (isAdminLogin ? 'Access Admin Panel' : 'Sign In') }}
          </button>
        </form>
        <div v-if="demoLoginAvailable" class="d-grid gap-2 mb-3">
          <button
            v-for="demo in demoAccounts"
            :key="demo.role"
            type="button"
            class="btn btn-outline-primary"
            :disabled="authStore.isLoading"
            @click="handleLogin(demo.role)"
          >
            <span v-if="pendingDemoRole === demo.role" class="spinner-border spinner-border-sm me-2"></span>
            {{ demo.label }}
          </button>
        </div>
        <div class="text-center mb-3">
          <a href="#" class="forgot-password-link" @click="showForgotPassword">
            <i class="fas fa-key me-1"></i>Forgot your password?
          </a>
        </div>
        <div v-if="!isAdminLogin" class="divider">
          <span>or</span>
        </div>
        <div v-if="!isAdminLogin" class="text-center">
          <p class="mb-0">Don't have an account?</p>
          <router-link to="/register" class="register-link">
            <i class="fas fa-user-plus me-1"></i>Create your parking account
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
export default {
  name: 'LoginForm',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const isAdminLogin = ref(false)
    const demoLoginAvailable = ref(false)
    const pendingDemoRole = ref(null)
    const demoAccounts = [
      { role: 'user', label: 'Sign in as Demo User' },
      { role: 'admin', label: 'Sign in as Demo Admin' }
    ]
    const showPassword = ref(false)
    const form = reactive({
      username: '',
      password: '',
      rememberMe: false
    })
    const errors = reactive({
      username: '',
      password: ''
    })
    const isFormValid = computed(() => {
      return form.username.trim() && form.password.trim() && !authStore.isLoading
    })
    const validateForm = () => {
      errors.username = ''
      errors.password = ''
      if (!form.username.trim()) {
        errors.username = 'Username is required'
        return false
      }
      if (form.username.length < 3) {
        errors.username = 'Username must be at least 3 characters'
        return false
      }
      if (!form.password.trim()) {
        errors.password = 'Password is required'
        return false
      }
      if (form.password.length < 6) {
        errors.password = 'Password must be at least 6 characters'
        return false
      }
      return true
    }
    const handleLogin = async (demoRole = null) => {
      if (authStore.isLoading || (!demoRole && !validateForm())) return
      pendingDemoRole.value = demoRole
      try {
        const result = demoRole
          ? await authStore.loginAsDemo(demoRole)
          : await authStore.login({ username: form.username.trim(), password: form.password }, isAdminLogin.value)
        if (result.success) {
          const dashboard = result.user.is_admin ? '/admin/dashboard' : '/user/dashboard'
          await router.push(demoRole ? dashboard : route.query.redirect || dashboard)
        }
      } catch (error) {
        console.error('Login error:', error)
      } finally {
        pendingDemoRole.value = null
      }
    }
    const setLoginType = (isAdmin) => {
      isAdminLogin.value = isAdmin
      authStore.clearErrors()
      form.username = ''
      form.password = ''
      errors.username = ''
      errors.password = ''
    }
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }
    const showForgotPassword = () => {
      alert('Forgot password functionality will be implemented')
    }
    onMounted(async () => {
      authStore.clearErrors()
      if (authStore.isAuthenticated) {
        const redirectPath = authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'
        router.push(redirectPath)
        return
      }
      demoLoginAvailable.value = await authStore.isDemoLoginAvailable()
    })
    return {
      authStore,
      isAdminLogin,
      demoLoginAvailable,
      pendingDemoRole,
      demoAccounts,
      showPassword,
      form,
      errors,
      isFormValid,
      handleLogin,
      setLoginType,
      togglePasswordVisibility,
      showForgotPassword
    }
  }
}
</script>
<style scoped>
.login-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  padding: 2rem 1rem;
}
.login-card {
  width: 100%;
  max-width: 420px;
  border: none;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 1, 51, 0.3);
  overflow: hidden;
}
.card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: none;
  padding: 2rem 2rem 1rem;
}
.app-logo {
  font-size: 3rem;
  color: var(--secondary-color);
}
.card-title {
  color: var(--primary-color);
  font-weight: 700;
}
.card-subtitle {
  color: #666;
  font-size: 0.9rem;
}
.card-body {
  padding: 2rem;
}
.login-type-toggle .btn-outline-primary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}
.login-type-toggle .btn-check:checked + .btn-outline-primary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
.form-label {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.form-control {
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}
.form-control:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 10px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(75, 0, 110, 0.4);
}
.btn-primary:disabled {
  opacity: 0.7;
  transform: none;
}
.forgot-password-link {
  color: var(--secondary-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}
.forgot-password-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}
.divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
  color: #999;
}
.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #ddd;
}
.divider span {
  background: white;
  padding: 0 1rem;
  position: relative;
}
.register-link {
  color: var(--secondary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}
.register-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}
.alert-danger {
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(255, 255, 255, 0.9));
  border-left: 4px solid #dc3545;
}
.form-check-input:checked {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.input-group .btn-outline-secondary {
  border-color: rgba(138, 184, 254, 0.3);
  color: var(--secondary-color);
}
.input-group .btn-outline-secondary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
@media (max-width: 576px) {
  .login-form-container {
    padding: 1rem 0.5rem;
  }
  .card-header,
  .card-body {
    padding: 1.5rem;
  }
}
.form-control,
.btn {
  transition: all 0.3s ease;
}
.form-control:focus {
  transform: translateY(-1px);
}
.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
