<template>
  <div class="login-page">
    
    <div class="auth-background"></div>
    
    <nav class="navbar navbar-light bg-transparent position-absolute w-100" style="z-index: 10;">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <i class="fas fa-car me-2 text-white"></i>
          <span class="text-white fw-bold">ParkSmart</span>
        </router-link>
        <div class="nav-actions">
          <router-link to="/" class="btn btn-outline-light btn-sm me-2">
            <i class="fas fa-arrow-left me-1"></i>Back to Home
          </router-link>
        </div>
      </div>
    </nav>
    
    <div class="container-fluid h-100">
      <div class="row h-100">
        
        <div class="col-lg-6 d-none d-lg-flex branding-section">
          <div class="branding-content">
            <div class="brand-logo mb-4">
              <i class="fas fa-parking text-accent"></i>
              <h2 class="brand-name">Welcome Back to ParkSmart</h2>
            </div>
            <div class="brand-features">
              <div class="feature-item">
                <div class="feature-icon">
                  <i class="fas fa-search"></i>
                </div>
                <div class="feature-text">
                  <h6>Smart Search</h6>
                  <p>Find parking spots instantly near your destination</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <i class="fas fa-mobile-alt"></i>
                </div>
                <div class="feature-text">
                  <h6>Mobile Friendly</h6>
                  <p>Book and manage reservations on any device</p>
                </div>
              </div>
              <div class="feature-item">
                <div class="feature-icon">
                  <i class="fas fa-clock"></i>
                </div>
                <div class="feature-text">
                  <h6>Save Time</h6>
                  <p>No more circling around looking for parking</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-6 form-section">
          <div class="form-container">
            <div class="form-header text-center mb-4">
              <div class="form-logo d-lg-none mb-3">
                <i class="fas fa-car text-primary"></i>
                <h4 class="text-primary">ParkSmart</h4>
              </div>
              <h3 class="form-title">Sign In to Your Account</h3>
              <p class="form-subtitle">Access your parking dashboard and manage reservations</p>
            </div>
            
            <LoginForm />
            <div class="form-footer text-center mt-4">
              <div class="divider mb-3">
                <span>New to ParkSmart?</span>
              </div>
              <router-link to="/register" class="btn btn-outline-primary">
                <i class="fas fa-user-plus me-2"></i>
                Create Your Account
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
import LoginForm from '../../components/auth/LoginForm.vue'
export default {
  name: 'Login',
  components: {
    LoginForm
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const showHelp = () => {
      alert('Help documentation will be available here')
    }
    const showSupport = () => {
      alert('Contact support: support@parksmart.com')
    }
    onMounted(() => {
      if (authStore.isAuthenticated) {
        const redirectPath = authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'
        router.push(redirectPath)
      }
    })
    return {
      showHelp,
      showSupport
    }
  }
}
</script>
<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  position: relative;
}
.auth-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(138, 184, 254, 0.1) 2px, transparent 2px),
    radial-gradient(circle at 80% 40%, rgba(138, 184, 254, 0.1) 2px, transparent 2px),
    radial-gradient(circle at 40% 80%, rgba(138, 184, 254, 0.1) 2px, transparent 2px);
  background-size: 100px 100px;
  animation: float 20s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}
.navbar-brand {
  font-size: 1.5rem;
  text-decoration: none;
  color: white !important;
}
.branding-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  z-index: 2;
}
.branding-content {
  max-width: 500px;
  color: white;
}
.brand-logo {
  text-align: center;
}
.brand-logo i {
  font-size: 4rem;
  color: var(--text-accent);
  margin-bottom: 1rem;
  display: block;
}
.brand-name {
  color: var(--text-accent);
  font-weight: 700;
  margin-bottom: 2rem;
}
.brand-features {
  margin-bottom: 2rem;
}
.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}
.feature-icon {
  width: 50px;
  height: 50px;
  background: rgba(138, 184, 254, 0.2);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: var(--text-accent);
  margin-right: 1rem;
}
.feature-text h6 {
  color: var(--text-accent);
  margin-bottom: 0.25rem;
  font-weight: 600;
}
.feature-text p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 0.9rem;
}
.brand-stats {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}
.stat-number {
  color: var(--text-accent);
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.25rem;
}
.stat-label {
  color: rgba(255, 255, 255, 0.8);
}
.testimonial {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border-left: 4px solid var(--text-accent);
}
.testimonial-text {
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 1rem;
}
.testimonial-author {
  color: var(--text-accent);
  font-size: 0.9rem;
}
.form-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}
.form-container {
  width: 100%;
  max-width: 480px;
}
.form-logo i {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}
.form-title {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.form-subtitle {
  color: #6c757d;
  margin-bottom: 2rem;
}
.divider {
  position: relative;
  text-align: center;
  color: #6c757d;
  font-size: 0.9rem;
}
.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: #dee2e6;
  z-index: 1;
}
.divider span {
  background: rgba(255, 255, 255, 0.95);
  padding: 0 1rem;
  position: relative;
  z-index: 2;
}
.btn-outline-primary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
  border-radius: 8px;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
}
.btn-outline-primary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
.help-links {
  margin-top: 1rem;
}
.help-link {
  color: var(--secondary-color);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}
.help-link:hover {
  color: var(--primary-color);
  text-decoration: underline;
}
@media (max-width: 991px) {
  .branding-section {
    display: none;
  }
  .form-section {
    background: rgba(255, 255, 255, 0.95);
  }
}
@media (max-width: 768px) {
  .login-page {
    padding-top: 80px;
  }
  .form-container {
    padding: 1rem;
  }
  .form-title {
    font-size: 1.75rem;
  }
}
</style>