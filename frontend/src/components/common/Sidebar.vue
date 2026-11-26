<template>
  <aside class="app-sidebar" :class="{ 'collapsed': isCollapsed }">
    <div class="sidebar-content">
      
      <div class="sidebar-header">
        <div class="sidebar-brand">
          <i class="fas fa-car brand-icon"></i>
          <span v-if="!isCollapsed" class="brand-text">ParkSmart</span>
        </div>
        <button
          class="btn btn-sm btn-outline-light toggle-btn"
          @click="toggleSidebar"
          :title="isCollapsed ? 'Expand Sidebar' : 'Collapse Sidebar'"
        >
          <i class="fas" :class="isCollapsed ? 'fa-chevron-right' : 'fa-chevron-left'"></i>
        </button>
      </div>
      
      <div v-if="authStore.isAuthenticated" class="user-section">
        <div class="user-avatar">
          <i class="fas fa-user-circle"></i>
        </div>
        <div v-if="!isCollapsed" class="user-info">
          <div class="user-name">{{ authStore.userName }}</div>
          <div class="user-role">
            <span class="role-badge">
              {{ authStore.isAdmin ? 'Administrator' : 'User' }}
            </span>
          </div>
        </div>
      </div>
      
      <nav class="sidebar-nav">
        <ul class="nav-list">
          
          <template v-if="authStore.isAdmin">
            <li class="nav-section-title" v-if="!isCollapsed">
              <i class="fas fa-cogs me-2"></i>Administration
            </li>
            <li class="nav-item">
              <router-link to="/admin/dashboard" class="nav-link" :title="isCollapsed ? 'Dashboard' : ''">
                <i class="fas fa-tachometer-alt nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Dashboard</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/parking-lots" class="nav-link" :title="isCollapsed ? 'Parking Lots' : ''">
                <i class="fas fa-building nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Parking Lots</span>
                <span v-if="!isCollapsed && parkingLotsCount > 0" class="nav-badge">
                  {{ parkingLotsCount }}
                </span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/admin/users" class="nav-link" :title="isCollapsed ? 'Users' : ''">
                <i class="fas fa-users nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Users</span>
                <span v-if="!isCollapsed && usersCount > 0" class="nav-badge">
                  {{ usersCount }}
                </span>
              </router-link>
            </li>
          </template>
          
          <template v-else-if="authStore.isAuthenticated">
            <li class="nav-section-title" v-if="!isCollapsed">
              <i class="fas fa-user me-2"></i>My Account
            </li>
            <li class="nav-item">
              <router-link to="/user/dashboard" class="nav-link" :title="isCollapsed ? 'Dashboard' : ''">
                <i class="fas fa-tachometer-alt nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Dashboard</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/reserve-parking" class="nav-link" :title="isCollapsed ? 'Reserve Parking' : ''">
                <i class="fas fa-parking nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Reserve Parking</span>
                <span v-if="!isCollapsed && hasActiveReservation" class="nav-badge active">
                  Active
                </span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/my-bookings" class="nav-link" :title="isCollapsed ? 'My Bookings' : ''">
                <i class="fas fa-history nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">My Bookings</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/user/statistics" class="nav-link" :title="isCollapsed ? 'Statistics' : ''">
                <i class="fas fa-chart-line nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Statistics</span>
              </router-link>
            </li>
          </template>
          
          <template v-else>
            <li class="nav-item">
              <router-link to="/" class="nav-link" :title="isCollapsed ? 'Home' : ''">
                <i class="fas fa-home nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Home</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/login" class="nav-link" :title="isCollapsed ? 'Login' : ''">
                <i class="fas fa-sign-in-alt nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Login</span>
              </router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="nav-link" :title="isCollapsed ? 'Register' : ''">
                <i class="fas fa-user-plus nav-icon"></i>
                <span v-if="!isCollapsed" class="nav-text">Register</span>
              </router-link>
            </li>
          </template>
        </ul>
      </nav>
      
      <div v-if="authStore.isAuthenticated && !isCollapsed" class="quick-actions">
        <div class="section-title">Quick Actions</div>
        <div class="action-buttons">
          <button v-if="!authStore.isAdmin" class="btn btn-primary-custom btn-sm w-100 mb-2" @click="quickReserve">
            <i class="fas fa-plus me-1"></i>Quick Reserve
          </button>
          <button v-if="authStore.isAdmin" class="btn btn-secondary-custom btn-sm w-100 mb-2" @click="addParkingLot">
            <i class="fas fa-plus me-1"></i>Add Parking Lot
          </button>
          <button class="btn btn-outline-light btn-sm w-100" @click="exportData">
            <i class="fas fa-download me-1"></i>Export Data
          </button>
        </div>
      </div>
    </div>
    
    <div class="sidebar-footer">
      <div v-if="!isCollapsed" class="app-status">
        <small class="text-muted">
          <i class="fas fa-circle text-success me-1"></i>
          System Online
        </small>
      </div>
    </div>
  </aside>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/modules/auth'
import { useAdminStore } from '../../store/modules/admin'
import { useParkingStore } from '../../store/modules/parking'
export default {
  name: 'Sidebar',
  props: {
    defaultCollapsed: {
      type: Boolean,
      default: false
    }
  },
  emits: ['toggle'],
  setup(props, { emit }) {
    const router = useRouter()
    const authStore = useAuthStore()
    const adminStore = useAdminStore()
    const parkingStore = useParkingStore()
    const isCollapsed = ref(props.defaultCollapsed)
    const parkingLotsCount = computed(() => adminStore.parkingLots.length)
    const usersCount = computed(() => adminStore.users.length)
    const hasActiveReservation = computed(() => parkingStore.hasActiveReservation)
    const toggleSidebar = () => {
      isCollapsed.value = !isCollapsed.value
      emit('toggle', isCollapsed.value)
    }
    const quickReserve = () => {
      router.push('/user/reserve-parking')
    }
    const addParkingLot = () => {
      router.push('/admin/parking-lots')
    }
    const exportData = () => {
      if (authStore.isAdmin) {
        console.log('Export admin data')
      } else {
        parkingStore.exportParkingHistory()
      }
    }
    onMounted(() => {
      if (authStore.isAuthenticated) {
        if (authStore.isAdmin) {
          adminStore.fetchParkingLots()
          adminStore.fetchUsers()
        } else {
          parkingStore.fetchActiveReservation()
        }
      }
    })
    return {
      authStore,
      isCollapsed,
      parkingLotsCount,
      usersCount,
      hasActiveReservation,
      toggleSidebar,
      quickReserve,
      addParkingLot,
      exportData
    }
  }
}
</script>
<style scoped>
.app-sidebar {
  background: linear-gradient(180deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  height: 100vh;
  width: 280px;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 10px rgba(0, 1, 51, 0.1);
}
.app-sidebar.collapsed {
  width: 70px;
}
.sidebar-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
}
.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(138, 184, 254, 0.2);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  color: var(--text-accent);
  font-weight: bold;
  font-size: 1.2rem;
}
.brand-icon {
  font-size: 1.5rem;
  margin-right: 0.5rem;
}
.toggle-btn {
  border: 1px solid rgba(138, 184, 254, 0.3);
  color: var(--text-accent);
  padding: 4px 8px;
  font-size: 0.8rem;
}
.toggle-btn:hover {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: var(--text-accent);
}
.user-section {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(138, 184, 254, 0.2);
  display: flex;
  align-items: center;
}
.user-avatar {
  font-size: 2rem;
  color: var(--text-accent);
  margin-right: 0.75rem;
}
.user-name {
  font-weight: 600;
  color: white;
  font-size: 0.9rem;
}
.role-badge {
  background: rgba(138, 184, 254, 0.2);
  color: var(--text-accent);
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
}
.sidebar-nav {
  padding: 1rem 0;
}
.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.nav-section-title {
  padding: 0.5rem 1.5rem;
  font-size: 0.8rem;
  text-transform: uppercase;
  color: rgba(138, 184, 254, 0.7);
  font-weight: 600;
  margin-top: 1rem;
}
.nav-item {
  margin: 0.25rem 0;
}
.nav-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  color: rgba(138, 184, 254, 0.9);
  text-decoration: none;
  transition: all 0.3s ease;
  position: relative;
}
.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
  transform: translateX(3px);
}
.nav-link.router-link-active {
  background-color: rgba(138, 184, 254, 0.2);
  color: white;
  border-right: 3px solid var(--text-accent);
}
.nav-icon {
  font-size: 1.1rem;
  width: 20px;
  margin-right: 0.75rem;
  text-align: center;
}
.nav-badge {
  background-color: var(--secondary-color);
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
  margin-left: auto;
}
.nav-badge.active {
  background-color: #28a745;
  animation: pulse 2s infinite;
}
.quick-actions {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(138, 184, 254, 0.2);
  margin-top: auto;
}
.section-title {
  font-size: 0.8rem;
  text-transform: uppercase;
  color: rgba(138, 184, 254, 0.7);
  font-weight: 600;
  margin-bottom: 0.75rem;
}
.btn-primary-custom {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  color: white;
}
.btn-secondary-custom {
  background-color: var(--secondary-color);
  border: none;
  color: white;
}
.btn-outline-light {
  border: 1px solid rgba(138, 184, 254, 0.3);
  color: var(--text-accent);
}
.btn-outline-light:hover {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: var(--text-accent);
}
.sidebar-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid rgba(138, 184, 254, 0.2);
}
@media (max-width: 768px) {
  .app-sidebar {
    transform: translateX(-100%);
  }
  .app-sidebar.show {
    transform: translateX(0);
  }
}
.sidebar-content::-webkit-scrollbar {
  width: 4px;
}
.sidebar-content::-webkit-scrollbar-track {
  background: rgba(138, 184, 254, 0.1);
}
.sidebar-content::-webkit-scrollbar-thumb {
  background: rgba(138, 184, 254, 0.3);
  border-radius: 2px;
}
.sidebar-content::-webkit-scrollbar-thumb:hover {
  background: rgba(138, 184, 254, 0.5);
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>