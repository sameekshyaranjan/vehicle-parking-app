<template>
  <div id="app" class="min-vh-100">
    
    <nav v-if="showNavigation" class="navbar navbar-expand-lg navbar-dark bg-gradient-primary shadow-lg">
      <div class="container">
        
        <router-link to="/" class="navbar-brand">
          <i class="fas fa-car me-2"></i>
          <span class="fw-bold">ParkSmart</span>
        </router-link>
        
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            
            <template v-if="isUserAdmin">
              <li class="nav-item">
                <router-link to="/admin/dashboard" class="nav-link">
                  <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/parking-lots" class="nav-link">
                  <i class="fas fa-building me-1"></i>Parking Lots
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/admin/users" class="nav-link">
                  <i class="fas fa-users me-1"></i>Users
                </router-link>
              </li>
              
            </template>
            
            <template v-else-if="isAuthenticated">
              <li class="nav-item">
                <router-link to="/user/dashboard" class="nav-link">
                  <i class="fas fa-tachometer-alt me-1"></i>Dashboard
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/user/reserve-parking" class="nav-link">
                  <i class="fas fa-parking me-1"></i>Reserve Parking
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/user/my-bookings" class="nav-link">
                  <i class="fas fa-history me-1"></i>My Bookings
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/user/statistics" class="nav-link">
                  <i class="fas fa-chart-line me-1"></i>Statistics
                </router-link>
              </li>
            </template>
          </ul>
          
          <div class="navbar-nav">
            <template v-if="isAuthenticated">
              
              <div class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle text-accent"
                  href="#"
                  id="userDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i class="fas fa-user-circle me-1"></i>
                  {{ currentUser.fullname || currentUser.username }}
                </a>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li>
                    <h6 class="dropdown-header">
                      <span class="badge bg-secondary me-2">
                        {{ isUserAdmin ? 'Admin' : 'User' }}
                      </span>
                      {{ currentUser.email }}
                    </h6>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click="handleLogout">
                      <i class="fas fa-sign-out-alt me-2"></i>Logout
                    </a>
                  </li>
                </ul>
              </div>
            </template>
            
            <template v-else>
              <li class="nav-item">
                <router-link to="/login" class="nav-link">
                  <i class="fas fa-sign-in-alt me-1"></i>Login
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/register" class="nav-link">
                  <i class="fas fa-user-plus me-1"></i>Register
                </router-link>
              </li>
            </template>
          </div>
        </div>
      </div>
    </nav>
    
    <main class="flex-grow-1">
      
      <div v-if="isLoading" class="loading-overlay">
        <div class="text-center">
          <div class="parking-spinner mx-auto mb-3"></div>
          <h5 class="text-white">{{ loadingMessage }}</h5>
        </div>
      </div>
      
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer v-if="showFooter" class="bg-primary text-accent py-4 mt-auto">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h6 class="fw-bold">🚗 Vehicle Parking App V2</h6>
            <p class="mb-0 small opacity-75">Smart parking solutions for modern cities</p>
          </div>
          <div class="col-md-6 text-md-end">
            <small class="opacity-75">
              &copy; {{ currentYear }} ParkSmart. All rights reserved.
            </small>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>
<script>
import { computed, ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const route = useRoute()
    const isLoading = ref(false)
    const loadingMessage = ref('Loading...')
    const isAuthenticated = computed(() => {
      return !!localStorage.getItem('access_token')
    })
    const currentUser = computed(() => {
      return JSON.parse(localStorage.getItem('user') || '{}')
    })
    const isUserAdmin = computed(() => {
      return currentUser.value.is_admin === true
    })
    const showNavigation = computed(() => {
      const hideNavRoutes = ['/login', '/register']
      return !hideNavRoutes.includes(route.path)
    })
    const showFooter = computed(() => {
      return showNavigation.value
    })
    const currentYear = computed(() => {
      return new Date().getFullYear()
    })
    const handleLogout = async () => {
      if (confirm('Are you sure you want to logout?')) {
        isLoading.value = true
        loadingMessage.value = 'Logging out...'
        try {
          await fetch('/api/auth/logout', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            }
          })
        } catch (error) {
          console.error('Logout error:', error)
        } finally {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
          router.push('/login')
          isLoading.value = false
        }
      }
    }
    const changePassword = () => {
      alert('Password change functionality will be implemented')
    }
    onMounted(() => {
      if (!isAuthenticated.value && route.meta.requiresAuth) {
        router.push('/login')
      }
    })
    watch(route, (to) => {
      document.title = to.meta.title ?
        `${to.meta.title} - Vehicle Parking App V2` :
        'Vehicle Parking App V2'
      if (to.meta.requiresAuth && !isAuthenticated.value) {
        router.push('/login')
      }
      if (to.meta.requiresAdmin && !isUserAdmin.value) {
        router.push(isAuthenticated.value ? '/user/dashboard' : '/login')
      }
    })
    return {
      isLoading,
      loadingMessage,
      isAuthenticated,
      currentUser,
      isUserAdmin,
      showNavigation,
      showFooter,
      currentYear,
      handleLogout,
      changePassword
    }
  }
}
</script>
<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 1, 51, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.page-enter-active,
.page-leave-active {
  transition: all 0.3s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
.page-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
.navbar-brand {
  font-size: 1.5rem;
  color: var(--text-accent) !important;
}
.nav-link {
  color: var(--text-accent) !important;
  transition: all 0.3s ease;
}
.nav-link:hover {
  color: white !important;
  transform: translateY(-1px);
}
.nav-link.router-link-active {
  color: white !important;
  font-weight: 600;
}
.dropdown-menu {
  border: none;
  box-shadow: 0 10px 30px rgba(0,1,51,0.2);
  border-radius: 10px;
}
.dropdown-item:hover {
  background-color: var(--secondary-color);
  color: white;
}
footer {
  background: var(--primary-color) !important;
}
@media (max-width: 768px) {
  .navbar-brand {
    font-size: 1.25rem;
  }
  .nav-link {
    padding: 0.75rem 1rem;
  }
}
</style>