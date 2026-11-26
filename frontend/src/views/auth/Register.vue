<template>
  <div class="register-page">
    
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
          <router-link to="/login" class="btn btn-light btn-sm">
            <i class="fas fa-sign-in-alt me-1"></i>Sign In
          </router-link>
        </div>
      </div>
    </nav>
    
    <div class="container-fluid h-100">
      <div class="row h-100">
        
        <div class="col-lg-6 d-none d-lg-flex benefits-section">
          <div class="benefits-content">
            <div class="benefits-header mb-4">
              <div class="benefits-logo mb-3">
                <i class="fas fa-user-plus text-accent"></i>
              </div>
              <h2 class="benefits-title">Join the Smart Parking Revolution</h2>
              <p class="benefits-subtitle">
                Create your account and discover a smarter way to park
              </p>
            </div>
            <div class="benefits-list">
              <div class="benefit-item">
                <div class="benefit-icon">
                  <i class="fas fa-gift"></i>
                </div>
                <div class="benefit-text">
                  <h6>Welcome Bonus</h6>
                  <p>Get ₹100 parking credits when you sign up</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-icon">
                  <i class="fas fa-map-marked-alt"></i>
                </div>
                <div class="benefit-text">
                  <h6>500+ Locations</h6>
                  <p>Access to premium parking spots across the city</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-icon">
                  <i class="fas fa-bell"></i>
                </div>
                <div class="benefit-text">
                  <h6>Smart Notifications</h6>
                  <p>Never miss a booking with timely reminders</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-icon">
                  <i class="fas fa-chart-line"></i>
                </div>
                <div class="benefit-text">
                  <h6>Usage Analytics</h6>
                  <p>Track your parking patterns and save money</p>
                </div>
              </div>
              <div class="benefit-item">
                <div class="benefit-icon">
                  <i class="fas fa-shield-alt"></i>
                </div>
                <div class="benefit-text">
                  <h6>Secure & Reliable</h6>
                  <p>Your data is protected with enterprise-grade security</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="col-lg-6 form-section">
          <div class="form-container">
            <div class="form-header text-center mb-4">
              <div class="form-logo d-lg-none mb-3">
                <i class="fas fa-user-plus text-primary"></i>
                <h4 class="text-primary">Join ParkSmart</h4>
              </div>
              <h3 class="form-title">Create Your Account</h3>
              <p class="form-subtitle">
                Start your smart parking journey today - it only takes a minute!
              </p>
              
              <div class="registration-progress mb-4">
                <div class="progress-steps">
                  <div class="step active">
                    <div class="step-circle">1</div>
                    <small>Account Info</small>
                  </div>
                  <div class="step-line"></div>
                  <div class="step">
                    <div class="step-circle">2</div>
                    <small>Verification</small>
                  </div>
                  <div class="step-line"></div>
                  <div class="step">
                    <div class="step-circle">3</div>
                    <small>Welcome</small>
                  </div>
                </div>
              </div>
            </div>
            
            <RegisterForm @registration-success="handleRegistrationSuccess" />
            <div class="form-footer text-center mt-4">
              <div class="security-notice mb-3">
                <i class="fas fa-lock text-success me-2"></i>
                <small class="text-muted">
                  Your information is encrypted and secure
                </small>
              </div>
              <div class="divider mb-3">
                <span>Already have an account?</span>
              </div>
              <router-link to="/login" class="btn btn-outline-primary">
                <i class="fas fa-sign-in-alt me-2"></i>
                Sign In Instead
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showWelcome" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">
              <i class="fas fa-party-horn me-2"></i>
              Welcome to ParkSmart!
            </h5>
          </div>
          <div class="modal-body text-center">
            <div class="welcome-animation mb-4">
              <i class="fas fa-car welcome-icon"></i>
              <div class="confetti"></div>
            </div>
            <h4 class="welcome-title">Congratulations! 🎉</h4>
            <p class="welcome-message">
              Your account has been created successfully. You're now part of the
              ParkSmart community with access to smart parking solutions.
            </p>
            <div class="welcome-benefits">
              <h6 class="text-primary mb-3">What's Next?</h6>
              <div class="row">
                <div class="col-md-4">
                  <div class="next-step">
                    <i class="fas fa-search text-primary"></i>
                    <h6>Explore Locations</h6>
                    <small>Find parking spots near you</small>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="next-step">
                    <i class="fas fa-calendar-check text-success"></i>
                    <h6>Make Your First Booking</h6>
                    <small>Reserve your first parking spot</small>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="next-step">
                    <i class="fas fa-gift text-warning"></i>
                    <h6>Claim Welcome Bonus</h6>
                    <small>Get ₹100 parking credits</small>
                  </div>
                </div>
              </div>
            </div>
            <div class="bonus-info mt-4">
              <div class="bonus-card">
                <i class="fas fa-coins text-warning me-2"></i>
                <strong>Welcome Bonus: ₹100 Parking Credits</strong>
                <small class="d-block text-muted">Automatically added to your account</small>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="startParkingJourney">
              <i class="fas fa-rocket me-1"></i>Start Parking Journey
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showWelcome" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
import RegisterForm from '../../components/auth/RegisterForm.vue'
export default {
  name: 'Register',
  components: {
    RegisterForm
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const showWelcome = ref(false)
    const handleRegistrationSuccess = (userData) => {
      showWelcome.value = true
      setTimeout(() => {
        if (showWelcome.value) {
          startParkingJourney()
        }
      }, 10000)
    }
    const startParkingJourney = () => {
      showWelcome.value = false
      router.push('/user/dashboard')
    }
    const showTerms = () => {
      alert('Terms of Service will be displayed here')
    }
    const showPrivacy = () => {
      alert('Privacy Policy will be displayed here')
    }
    const showSupport = () => {
      alert('Contact support: support@parksmart.com or call +91-800-PARKING')
    }
    onMounted(() => {
      if (authStore.isAuthenticated) {
        const redirectPath = authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'
        router.push(redirectPath)
      }
    })
    return {
      showWelcome,
      handleRegistrationSuccess,
      startParkingJourney,
      showTerms,
      showPrivacy,
      showSupport
    }
  }
}
</script>
<style scoped>
.register-page {
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
.benefits-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  z-index: 2;
}
.benefits-content {
  max-width: 500px;
  color: white;
}
.benefits-logo i {
  font-size: 4rem;
  color: var(--text-accent);
  display: block;
  text-align: center;
}
.benefits-title {
  color: var(--text-accent);
  font-weight: 700;
  margin-bottom: 1rem;
  text-align: center;
}
.benefits-subtitle {
  color: rgba(255, 255, 255, 0.9);
  text-align: center;
  margin-bottom: 2rem;
}
.benefits-list {
  margin-bottom: 2rem;
}
.benefit-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}
.benefit-item:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateX(5px);
}
.benefit-icon {
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
.benefit-text h6 {
  color: var(--text-accent);
  margin-bottom: 0.25rem;
  font-weight: 600;
}
.benefit-text p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 0.9rem;
}
.success-stories {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}
.stories-title {
  color: var(--text-accent);
  margin-bottom: 1rem;
  font-weight: 600;
}
.story-stats {
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}
.stat {
  text-align: center;
}
.stat h4 {
  color: var(--text-accent);
  font-weight: 700;
  margin-bottom: 0.25rem;
  font-size: 1.5rem;
}
.stat small {
  color: rgba(255, 255, 255, 0.8);
}
.story-quote {
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0.5rem;
  border: none;
  padding: 0;
}
.story-author {
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
  margin-bottom: 1rem;
}
.registration-progress {
  background: rgba(138, 184, 254, 0.1);
  padding: 1rem;
  border-radius: 10px;
}
.progress-steps {
  display: flex;
  align-items: center;
  justify-content: center;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.5;
}
.step.active {
  opacity: 1;
}
.step-circle {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #dee2e6;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.step.active .step-circle {
  background: var(--secondary-color);
  color: white;
}
.step-line {
  width: 40px;
  height: 2px;
  background: #dee2e6;
  margin: 0 10px;
}
.step small {
  font-size: 0.75rem;
  color: #6c757d;
  text-align: center;
}
.security-notice {
  background: rgba(40, 167, 69, 0.1);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  display: inline-block;
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
.welcome-animation {
  position: relative;
  display: inline-block;
}
.welcome-icon {
  font-size: 4rem;
  color: var(--secondary-color);
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}
.confetti {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 100px;
  background:
    radial-gradient(circle, #ffd700 2px, transparent 2px),
    radial-gradient(circle, #ff6b6b 2px, transparent 2px),
    radial-gradient(circle, #4ecdc4 2px, transparent 2px);
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px, 5px 15px;
  animation: confetti-fall 3s ease-out infinite;
}
@keyframes confetti-fall {
  0% { opacity: 1; transform: translateX(-50%) translateY(-20px) rotate(0deg); }
  100% { opacity: 0; transform: translateX(-50%) translateY(50px) rotate(360deg); }
}
.welcome-title {
  color: var(--primary-color);
  margin-bottom: 1rem;
}
.welcome-message {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}
.next-step {
  text-align: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.1);
  border-radius: 8px;
  margin-bottom: 1rem;
}
.next-step i {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}
.next-step h6 {
  color: var(--primary-color);
  margin-bottom: 0.5rem;
}
.next-step small {
  color: #6c757d;
}
.bonus-card {
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.1), rgba(255, 255, 255, 0.9));
  border: 2px solid #ffc107;
  border-radius: 10px;
  padding: 1rem;
  color: var(--primary-color);
}
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1040;
}
@media (max-width: 991px) {
  .benefits-section {
    display: none;
  }
  .form-section {
    background: rgba(255, 255, 255, 0.95);
  }
}
@media (max-width: 768px) {
  .register-page {
    padding-top: 80px;
  }
  .form-container {
    padding: 1rem;
  }
  .form-title {
    font-size: 1.75rem;
  }
  .progress-steps {
    justify-content: space-between;
  }
  .step-line {
    flex: 1;
    max-width: 60px;
  }
}
</style>