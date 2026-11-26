<template>
  <header class="app-header">
    <nav class="navbar navbar-expand-lg navbar-dark bg-gradient-primary shadow-lg">
      <div class="container-fluid">
        
        <router-link to="/" class="navbar-brand d-flex align-items-center">
          <div class="brand-icon me-2">
            <i class="fas fa-car"></i>
          </div>
          <div class="brand-text">
            <span class="brand-name">ParkSmart</span>
            <small class="brand-subtitle d-none d-md-block">V2</small>
          </div>
        </router-link>
        
        <button
          class="navbar-toggler custom-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#mainNavbar"
          aria-controls="mainNavbar"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="mainNavbar">
          
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            
            <template v-if="authStore.isAdmin">
              <li class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  id="adminDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  <i class="fas fa-cogs me-1"></i>Admin Panel
                </a>
                <ul class="dropdown-menu custom-dropdown">
                  <li>
                    <router-link to="/admin/dashboard" class="dropdown-item">2
                      <i class="fas fa-tachometer-alt me-2"></i>Dashboard
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/admin/parking-lots" class="dropdown-item">
                      <i class="fas fa-building me-2"></i>Parking Lots
                    </router-link>
                  </li>
                  <li>
                    <router-link to="/admin/users" class="dropdown-item">
                      <i class="fas fa-users me-2"></i>Manage Users
                    </router-link>
                  </li>
                </ul>
              </li>
            </template>
            
            <template v-else-if="authStore.isAuthenticated">
              <li class="nav-item">
                <router-link to="/user/dashboard" class="nav-link">
                  <i class="fas fa-tachometer-alt me-1"></i>
                  <span class="d-none d-lg-inline">Dashboard</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/user/reserve-parking" class="nav-link">
                  <i class="fas fa-parking me-1"></i>
                  <span class="d-none d-lg-inline">Reserve</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link to="/user/my-bookings" class="nav-link">
                  <i class="fas fa-history me-1"></i>
                  <span class="d-none d-lg-inline">My Bookings</span>
                </router-link>
              </li>
            </template>
          </ul>
          
          <div class="navbar-nav ms-auto">
            
            <div v-if="authStore.isAuthenticated" class="nav-item dropdown me-2">
              <a
                class="nav-link position-relative"
                href="#"
                id="notificationDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i class="fas fa-bell"></i>
                <span
                  v-if="unreadNotifications > 0"
                  class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger"
                >
                  {{ unreadNotifications }}
                </span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end custom-dropdown">
                <li class="dropdown-header">Notifications</li>
                <li v-if="notifications.length === 0">
                  <span class="dropdown-item-text text-muted">No new notifications</span>
                </li>
                <li v-for="notification in notifications" :key="notification.id">
                  <a class="dropdown-item" href="#">
                    <div class="d-flex">
                      <div class="flex-shrink-0">
                        <i :class="notification.icon" class="text-primary"></i>
                      </div>
                      <div class="flex-grow-1 ms-2">
                        <div class="fw-bold">{{ notification.title }}</div>
                        <small class="text-muted">{{ notification.time }}</small>
                      </div>
                    </div>
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-center" href="#">View all notifications</a>
                </li>
              </ul>
            </div>
            
            <div v-if="authStore.isAuthenticated" class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle user-dropdown"
                href="#"
                id="userDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <div class="user-avatar">
                  <i class="fas fa-user-circle"></i>
                </div>
                <span class="user-name d-none d-md-inline ms-2">
                  {{ authStore.userName }}
                </span>
              </a>
              <ul class="dropdown-menu dropdown-menu-end custom-dropdown">
                <li class="dropdown-header">
                  <div class="d-flex align-items-center">
                    <div class="user-avatar-large me-2">
                      <i class="fas fa-user-circle"></i>
                    </div>
                    <div>
                      <div class="fw-bold">{{ authStore.userName }}</div>
                      <small class="text-muted">{{ authStore.userEmail }}</small>
                      <div>
                        <span class="badge bg-secondary-custom">
                          {{ authStore.isAdmin ? 'Admin' : 'User' }}
                        </span>
                      </div>
                    </div>
                  </div>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#" @click="showProfile">
                    <i class="fas fa-user me-2"></i>My Profile
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click="showSettings">
                    <i class="fas fa-cog me-2"></i>Settings
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#" @click="showHelp">
                    <i class="fas fa-question-circle me-2"></i>Help & Support
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger" href="#" @click="handleLogout">
                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </div>
            
            <template v-else>
              <div class="nav-item me-2">
                <router-link to="/login" class="btn btn-outline-light btn-sm">
                  <i class="fas fa-sign-in-alt me-1"></i>Login
                </router-link>
              </div>
              <div class="nav-item">
                <router-link to="/register" class="btn btn-primary-custom btn-sm">
                  <i class="fas fa-user-plus me-1"></i>Register
                </router-link>
              </div>
            </template>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
export default {
  name: 'Header',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const notifications = ref([
      {
        id: 1,
        title: 'Parking spot reserved',
        time: '2 mins ago',
        icon: 'fas fa-parking text-success'
      },
      {
        id: 2,
        title: 'Monthly report ready',
        time: '1 hour ago',
        icon: 'fas fa-file-alt text-info'
      }
    ])
    const unreadNotifications = computed(() => notifications.value.length)
    const handleLogout = async () => {
      if (confirm('Are you sure you want to logout?')) {
        try {
          await authStore.logout()
          router.push('/')
        } catch (error) {
          console.error('Logout error:', error)
        }
      }
    }
    const showProfile = () => {
      console.log('Show profile modal/page')
    }
    const showSettings = () => {
      console.log('Show settings modal/page')
    }
    const showHelp = () => {
      console.log('Show help modal/page')
    }
    return {
      authStore,
      notifications,
      unreadNotifications,
      handleLogout,
      showProfile,
      showSettings,
      showHelp
    }
  }
}
</script>
<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
}
.bg-gradient-primary {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
}
.navbar-brand {
  font-weight: bold;
  color: var(--text-accent) !important;
  text-decoration: none;
}
.brand-icon {
  font-size: 2rem;
  color: var(--text-accent);
}
.brand-name {
  font-size: 1.5rem;
  font-weight: 700;
}
.brand-subtitle {
  font-size: 0.7rem;
  opacity: 0.8;
  margin-left: 0.25rem;
}
.nav-link {
  color: var(--text-accent) !important;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 2px;
  padding: 8px 12px !important;
}
.nav-link:hover {
  color: white !important;
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}
.nav-link.router-link-active {
  color: white !important;
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}
.custom-dropdown {
  border: none;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 1, 51, 0.2);
  background: white;
  min-width: 250px;
}
.dropdown-item {
  padding: 10px 16px;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 2px 8px;
}
.dropdown-item:hover {
  background-color: var(--secondary-color);
  color: white;
}
.dropdown-header {
  padding: 12px 16px;
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 8px;
  margin: 8px;
}
.user-dropdown {
  display: flex;
  align-items: center;
}
.user-avatar,
.user-avatar-large {
  font-size: 1.5rem;
  color: var(--text-accent);
}
.user-avatar-large {
  font-size: 2rem;
}
.custom-toggler {
  border: 2px solid var(--text-accent);
  border-radius: 8px;
}
.custom-toggler:focus {
  box-shadow: 0 0 0 0.25rem rgba(138, 184, 254, 0.25);
}
.btn-primary-custom {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(75, 0, 110, 0.4);
}
.btn-outline-light {
  border: 2px solid var(--text-accent);
  color: var(--text-accent);
  border-radius: 6px;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-outline-light:hover {
  background-color: var(--text-accent);
  border-color: var(--text-accent);
  color: var(--primary-color);
}
.bg-secondary-custom {
  background-color: var(--secondary-color) !important;
}
@media (max-width: 768px) {
  .brand-name {
    font-size: 1.25rem;
  }
  .brand-icon {
    font-size: 1.5rem;
  }
  .nav-link {
    margin: 2px 0;
  }
  .custom-dropdown {
    min-width: 200px;
  }
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.badge {
  animation: pulse 2s infinite;
}
</style>