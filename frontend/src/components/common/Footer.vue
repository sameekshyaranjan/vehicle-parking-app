<template>
  <footer class="app-footer bg-primary text-light py-4 mt-auto">
    <div class="container">
      <div class="row align-items-center">
        
        <div class="col-md-6 mb-3 mb-md-0">
          <div class="footer-brand d-flex align-items-center mb-2">
            <i class="fas fa-car me-2 text-accent"></i>
            <h6 class="mb-0 fw-bold text-accent">ParkSmart V2</h6>
          </div>
          <p class="mb-0 small opacity-75">
            Smart parking solutions for modern cities.
            Efficient, secure, and user-friendly vehicle parking management.
          </p>
        </div>
        
        <div class="col-md-3 mb-3 mb-md-0">
          <h6 class="fw-bold text-accent mb-2">Quick Links</h6>
          <ul class="list-unstyled footer-links">
            <li>
              <router-link to="/" class="footer-link">
                <i class="fas fa-home me-1"></i>Home
              </router-link>
            </li>
            <li v-if="!authStore.isAuthenticated">
              <router-link to="/login" class="footer-link">
                <i class="fas fa-sign-in-alt me-1"></i>Login
              </router-link>
            </li>
            <li v-if="!authStore.isAuthenticated">
              <router-link to="/register" class="footer-link">
                <i class="fas fa-user-plus me-1"></i>Register
              </router-link>
            </li>
            <li>
              <a href="#" class="footer-link" @click="showHelp">
                <i class="fas fa-question-circle me-1"></i>Help
              </a>
            </li>
            <li>
              <a href="#" class="footer-link" @click="showContact">
                <i class="fas fa-envelope me-1"></i>Contact
              </a>
            </li>
          </ul>
        </div>
        
        <div class="col-md-3">
          <h6 class="fw-bold text-accent mb-2">Connect With Us</h6>
          <div class="contact-info mb-2">
            <small class="d-block opacity-75">
              <i class="fas fa-envelope me-1"></i>
              support@parksmart.com
            </small>
            <small class="d-block opacity-75">
              <i class="fas fa-phone me-1"></i>
              +91-800-PARKING
            </small>
          </div>
          
          <div class="social-links">
            <a href="#" class="social-link me-2" title="Facebook">
              <i class="fab fa-facebook-f"></i>
            </a>
            <a href="#" class="social-link me-2" title="Twitter">
              <i class="fab fa-twitter"></i>
            </a>
            <a href="#" class="social-link me-2" title="LinkedIn">
              <i class="fab fa-linkedin-in"></i>
            </a>
            <a href="#" class="social-link" title="Instagram">
              <i class="fab fa-instagram"></i>
            </a>
          </div>
        </div>
      </div>
      <hr class="my-3 opacity-25">
      
      <div class="row align-items-center">
        <div class="col-md-6">
          <small class="opacity-75">
            &copy; {{ currentYear }} ParkSmart. All rights reserved.
            Powered by modern technology.
          </small>
        </div>
        <div class="col-md-6 text-md-end">
          <small class="opacity-75">
            <a href="#" class="footer-link me-3" @click="showPrivacy">Privacy Policy</a>
            <a href="#" class="footer-link me-3" @click="showTerms">Terms of Service</a>
            <span class="version-info">v{{ appVersion }}</span>
          </small>
        </div>
      </div>
      
      <div class="text-center mt-3">
        <small class="system-status">
          <span class="status-indicator" :class="systemStatus.class"></span>
          {{ systemStatus.message }}
        </small>
      </div>
    </div>
  </footer>
</template>
<script>
import { ref, computed } from 'vue'
import { useAuthStore } from '../../store/modules/auth'
export default {
  name: 'Footer',
  setup() {
    const authStore = useAuthStore()
    const appVersion = ref('2.0.0')
    const systemStatus = ref({
      class: 'status-online',
      message: 'All systems operational'
    })
    const currentYear = computed(() => new Date().getFullYear())
    const showHelp = () => {
      console.log('Show help center')
    }
    const showContact = () => {
      console.log('Show contact modal')
    }
    const showPrivacy = () => {
      console.log('Show privacy policy')
    }
    const showTerms = () => {
      console.log('Show terms of service')
    }
    return {
      authStore,
      appVersion,
      systemStatus,
      currentYear,
      showHelp,
      showContact,
      showPrivacy,
      showTerms
    }
  }
}
</script>
<style scoped>
.app-footer {
  background: var(--primary-color) !important;
  margin-top: auto;
}
.text-accent {
  color: var(--text-accent) !important;
}
.footer-brand {
  font-size: 1.1rem;
}
.footer-links {
  font-size: 0.9rem;
}
.footer-link {
  color: rgba(138, 184, 254, 0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
  padding: 2px 0;
}
.footer-link:hover {
  color: var(--text-accent);
  transform: translateX(3px);
}
.contact-info {
  font-size: 0.85rem;
}
.social-links {
  margin-top: 8px;
}
.social-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 35px;
  height: 35px;
  background: rgba(138, 184, 254, 0.1);
  color: var(--text-accent);
  border-radius: 50%;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}
.social-link:hover {
  background: var(--secondary-color);
  color: white;
  transform: translateY(-2px);
}
.system-status {
  color: rgba(138, 184, 254, 0.8);
  font-size: 0.8rem;
}
.status-indicator {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 6px;
}
.status-online {
  background-color: #28a745;
  box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.3);
  animation: pulse-green 2s infinite;
}
.status-offline {
  background-color: #dc3545;
}
.status-maintenance {
  background-color: #ffc107;
}
.version-info {
  color: rgba(138, 184, 254, 0.6);
  font-style: italic;
}
@keyframes pulse-green {
  0% {
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.7);
  }
  70% {
    box-shadow: 0 0 0 8px rgba(40, 167, 69, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(40, 167, 69, 0);
  }
}
@media (max-width: 768px) {
  .footer-brand {
    font-size: 1rem;
  }
  .social-link {
    width: 30px;
    height: 30px;
    font-size: 0.8rem;
  }
  .footer-links {
    margin-bottom: 1rem;
  }
}
</style>