<template>
  <div class="register-form-container">
    <div class="card register-card">
      <div class="card-header text-center">
        <div class="register-header">
          <div class="app-logo mb-3">
            <i class="fas fa-user-plus"></i>
          </div>
          <h4 class="card-title mb-1">Create Your Account</h4>
          <p class="card-subtitle">Join ParkSmart for seamless parking experience</p>
        </div>
      </div>
      <div class="card-body">
        
        <div v-if="authStore.registrationError" class="alert alert-danger alert-dismissible" role="alert">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ authStore.registrationError }}
          <button type="button" class="btn-close" @click="authStore.clearErrors()"></button>
        </div>
        
        <div v-if="showSuccess" class="alert alert-success" role="alert">
          <i class="fas fa-check-circle me-2"></i>
          Registration successful! Redirecting to dashboard...
        </div>
        
        <form @submit.prevent="handleRegister" novalidate>
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="username" class="form-label">
                <i class="fas fa-user me-1"></i>Username <span class="text-danger">*</span>
              </label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.username }"
                placeholder="Choose a username"
                required
                autocomplete="username"
                :disabled="authStore.isLoading"
                @blur="validateField('username')"
              >
              <div v-if="errors.username" class="invalid-feedback">
                {{ errors.username }}
              </div>
              <div class="form-text">3-50 characters, letters, numbers, and underscores only</div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="fullname" class="form-label">
                <i class="fas fa-id-card me-1"></i>Full Name <span class="text-danger">*</span>
              </label>
              <input
                id="fullname"
                v-model="form.fullname"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.fullname }"
                placeholder="Enter your full name"
                required
                autocomplete="name"
                :disabled="authStore.isLoading"
                @blur="validateField('fullname')"
              >
              <div v-if="errors.fullname" class="invalid-feedback">
                {{ errors.fullname }}
              </div>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="email" class="form-label">
              <i class="fas fa-envelope me-1"></i>Email Address <span class="text-danger">*</span>
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              :class="{ 'is-invalid': errors.email }"
              placeholder="Enter your email address"
              required
              autocomplete="email"
              :disabled="authStore.isLoading"
              @blur="validateField('email')"
            >
            <div v-if="errors.email" class="invalid-feedback">
              {{ errors.email }}
            </div>
          </div>
          
          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="password" class="form-label">
                <i class="fas fa-lock me-1"></i>Password <span class="text-danger">*</span>
              </label>
              <div class="input-group">
                <input
                  id="password"
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-control"
                  :class="{ 'is-invalid': errors.password }"
                  placeholder="Create a password"
                  required
                  autocomplete="new-password"
                  :disabled="authStore.isLoading"
                  @blur="validateField('password')"
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
              <div class="form-text">Minimum 6 characters</div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="confirmPassword" class="form-label">
                <i class="fas fa-lock me-1"></i>Confirm Password <span class="text-danger">*</span>
              </label>
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                class="form-control"
                :class="{ 'is-invalid': errors.confirmPassword }"
                placeholder="Confirm your password"
                required
                autocomplete="new-password"
                :disabled="authStore.isLoading"
                @blur="validateField('confirmPassword')"
              >
              <div v-if="errors.confirmPassword" class="invalid-feedback">
                {{ errors.confirmPassword }}
              </div>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="address" class="form-label">
              <i class="fas fa-map-marker-alt me-1"></i>Address <span class="text-danger">*</span>
            </label>
            <textarea
              id="address"
              v-model="form.address"
              class="form-control"
              :class="{ 'is-invalid': errors.address }"
              placeholder="Enter your complete address"
              rows="2"
              required
              :disabled="authStore.isLoading"
              @blur="validateField('address')"
            ></textarea>
            <div v-if="errors.address" class="invalid-feedback">
              {{ errors.address }}
            </div>
          </div>
          
          <div class="mb-4">
            <label for="pinCode" class="form-label">
              <i class="fas fa-map-pin me-1"></i>PIN Code <span class="text-danger">*</span>
            </label>
            <input
              id="pinCode"
              v-model="form.pin_code"
              type="text"
              class="form-control"
              :class="{ 'is-invalid': errors.pin_code }"
              placeholder="Enter 6-digit PIN code"
              required
              maxlength="6"
              :disabled="authStore.isLoading"
              @blur="validateField('pin_code')"
            >
            <div v-if="errors.pin_code" class="invalid-feedback">
              {{ errors.pin_code }}
            </div>
          </div>
          
          <div class="mb-4">
            <div class="form-check">
              <input
                id="termsAccepted"
                v-model="form.termsAccepted"
                type="checkbox"
                class="form-check-input"
                :class="{ 'is-invalid': errors.termsAccepted }"
                required
                :disabled="authStore.isLoading"
              >
              <label for="termsAccepted" class="form-check-label">
                I agree to the
                <a href="#" @click="showTerms" class="text-decoration-none">Terms of Service</a>
                and
                <a href="#" @click="showPrivacy" class="text-decoration-none">Privacy Policy</a>
                <span class="text-danger">*</span>
              </label>
              <div v-if="errors.termsAccepted" class="invalid-feedback d-block">
                {{ errors.termsAccepted }}
              </div>
            </div>
          </div>
          
          <div class="mb-4">
            <div class="form-check">
              <input
                id="newsletter"
                v-model="form.newsletter"
                type="checkbox"
                class="form-check-input"
                :disabled="authStore.isLoading"
              >
              <label for="newsletter" class="form-check-label">
                <i class="fas fa-envelope me-1"></i>
                Subscribe to parking updates and notifications
              </label>
            </div>
          </div>
          
          <button
            type="submit"
            class="btn btn-primary w-100 mb-3"
            :disabled="authStore.isLoading || !isFormValid"
          >
            <span v-if="authStore.isLoading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="fas fa-user-plus me-1"></i>
            {{ authStore.isLoading ? 'Creating Account...' : 'Create My Account' }}
          </button>
        </form>
        
        <div class="divider">
          <span>or</span>
        </div>
        
        <div class="text-center">
          <p class="mb-0">Already have an account?</p>
          <router-link to="/login" class="login-link">
            <i class="fas fa-sign-in-alt me-1"></i>Sign in to your account
          </router-link>
        </div>
        
        <div v-if="isDevelopment" class="demo-section mt-4">
          <h6 class="demo-title">Quick Demo</h6>
          <button
            type="button"
            class="btn btn-outline-secondary btn-sm w-100"
            @click="fillDemoData"
            :disabled="authStore.isLoading"
          >
            <i class="fas fa-magic me-1"></i>Fill Demo Data
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
export default {
  name: 'RegisterForm',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const showPassword = ref(false)
    const showSuccess = ref(false)
    const isDevelopment = ref(process.env.NODE_ENV === 'development')
    const form = reactive({
      username: '',
      fullname: '',
      email: '',
      password: '',
      confirmPassword: '',
      address: '',
      pin_code: '',
      termsAccepted: false,
      newsletter: true
    })
    const errors = reactive({
      username: '',
      fullname: '',
      email: '',
      password: '',
      confirmPassword: '',
      address: '',
      pin_code: '',
      termsAccepted: ''
    })
    const isFormValid = computed(() => {
      return form.username.trim() &&
             form.fullname.trim() &&
             form.email.trim() &&
             form.password.trim() &&
             form.confirmPassword.trim() &&
             form.address.trim() &&
             form.pin_code.trim() &&
             form.termsAccepted &&
             form.password === form.confirmPassword &&
             !Object.values(errors).some(error => error) &&
             !authStore.isLoading
    })
    const validateField = (fieldName) => {
      switch (fieldName) {
        case 'username':
          if (!form.username.trim()) {
            errors.username = 'Username is required'
          } else if (form.username.length < 3 || form.username.length > 50) {
            errors.username = 'Username must be between 3 and 50 characters'
          } else if (!/^[a-zA-Z0-9_]+$/.test(form.username)) {
            errors.username = 'Username can only contain letters, numbers, and underscores'
          } else {
            errors.username = ''
          }
          break
        case 'fullname':
          if (!form.fullname.trim()) {
            errors.fullname = 'Full name is required'
          } else if (form.fullname.length < 2 || form.fullname.length > 100) {
            errors.fullname = 'Full name must be between 2 and 100 characters'
          } else {
            errors.fullname = ''
          }
          break
        case 'email':
          const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/
          if (!form.email.trim()) {
            errors.email = 'Email address is required'
          } else if (!emailPattern.test(form.email)) {
            errors.email = 'Please enter a valid email address'
          } else {
            errors.email = ''
          }
          break
        case 'password':
          if (!form.password) {
            errors.password = 'Password is required'
          } else if (form.password.length < 6) {
            errors.password = 'Password must be at least 6 characters long'
          } else {
            errors.password = ''
          }
          break
        case 'confirmPassword':
          if (!form.confirmPassword) {
            errors.confirmPassword = 'Please confirm your password'
          } else if (form.password !== form.confirmPassword) {
            errors.confirmPassword = 'Passwords do not match'
          } else {
            errors.confirmPassword = ''
          }
          break
        case 'address':
          if (!form.address.trim()) {
            errors.address = 'Address is required'
          } else if (form.address.length < 10 || form.address.length > 500) {
            errors.address = 'Address must be between 10 and 500 characters'
          } else {
            errors.address = ''
          }
          break
        case 'pin_code':
          if (!form.pin_code.trim()) {
            errors.pin_code = 'PIN code is required'
          } else if (!/^\d{6}$/.test(form.pin_code)) {
            errors.pin_code = 'PIN code must be exactly 6 digits'
          } else {
            errors.pin_code = ''
          }
          break
        case 'termsAccepted':
          if (!form.termsAccepted) {
            errors.termsAccepted = 'You must accept the terms and conditions'
          } else {
            errors.termsAccepted = ''
          }
          break
      }
    }
    const validateAllFields = () => {
      Object.keys(form).forEach(field => {
        if (field !== 'newsletter') {
          validateField(field)
        }
      })
      return !Object.values(errors).some(error => error)
    }
    const handleRegister = async () => {
      if (!validateAllFields()) return
      try {
        const userData = {
          username: form.username.trim(),
          password: form.password,
          fullname: form.fullname.trim(),
          email: form.email.trim().toLowerCase(),
          address: form.address.trim(),
          pin_code: form.pin_code.trim()
        }
        const result = await authStore.register(userData)
        if (result.success) {
          showSuccess.value = true
          setTimeout(() => {
            router.push('/user/dashboard')
          }, 2000)
        }
      } catch (error) {
        console.error('Registration error:', error)
      }
    }
    const togglePasswordVisibility = () => {
      showPassword.value = !showPassword.value
    }
    const showTerms = () => {
      alert('Terms of Service will be displayed here')
    }
    const showPrivacy = () => {
      alert('Privacy Policy will be displayed here')
    }
    const fillDemoData = () => {
      form.username = 'demouser'
      form.fullname = 'Demo User'
      form.email = 'demo@example.com'
      form.password = 'demo123'
      form.confirmPassword = 'demo123'
      form.address = '123 Demo Street, Demo City, Demo State'
      form.pin_code = '123456'
      form.termsAccepted = true
    }
    onMounted(() => {
      authStore.clearErrors()
      if (authStore.isAuthenticated) {
        const redirectPath = authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'
        router.push(redirectPath)
      }
    })
    return {
      authStore,
      showPassword,
      showSuccess,
      isDevelopment,
      form,
      errors,
      isFormValid,
      validateField,
      handleRegister,
      togglePasswordVisibility,
      showTerms,
      showPrivacy,
      fillDemoData
    }
  }
}
</script>
<style scoped>
.register-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  padding: 2rem 1rem;
}
.register-card {
  width: 100%;
  max-width: 600px;
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
  max-height: 70vh;
  overflow-y: auto;
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
.form-text {
  font-size: 0.8rem;
  color: #666;
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
.form-check-input:checked {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
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
.login-link {
  color: var(--secondary-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}
.login-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}
.demo-section {
  background: rgba(138, 184, 254, 0.1);
  border-radius: 10px;
  padding: 1rem;
  border: 1px solid rgba(138, 184, 254, 0.3);
}
.demo-title {
  color: var(--primary-color);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.alert-success,
.alert-danger {
  border: none;
  border-radius: 10px;
}
.alert-success {
  background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(255, 255, 255, 0.9));
  border-left: 4px solid #28a745;
}
.alert-danger {
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(255, 255, 255, 0.9));
  border-left: 4px solid #dc3545;
}
.text-danger {
  color: #dc3545 !important;
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
.card-body::-webkit-scrollbar {
  width: 6px;
}
.card-body::-webkit-scrollbar-track {
  background: rgba(138, 184, 254, 0.1);
}
.card-body::-webkit-scrollbar-thumb {
  background: rgba(138, 184, 254, 0.3);
  border-radius: 3px;
}
.card-body::-webkit-scrollbar-thumb:hover {
  background: rgba(138, 184, 254, 0.5);
}
@media (max-width: 768px) {
  .register-form-container {
    padding: 1rem 0.5rem;
  }
  .card-header,
  .card-body {
    padding: 1.5rem;
  }
  .register-card {
    max-width: 100%;
  }
}
.form-control:focus {
  transform: translateY(-1px);
}
.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>