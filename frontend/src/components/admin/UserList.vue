<template>
  <div class="user-list">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary mb-1">
          <i class="fas fa-users me-2"></i>User Management
        </h4>
        <p class="text-muted mb-0">Manage and monitor registered users</p>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-primary" @click="refreshData">
          <i class="fas fa-sync me-1"></i>Refresh
        </button>
      </div>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-primary">
            <i class="fas fa-users"></i>
          </div>
          <div class="stats-content">
            <h6>Total Users</h6>
            <h4>{{ totalUsers }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-success">
            <i class="fas fa-user-check"></i>
          </div>
          <div class="stats-content">
            <h6>Active Users</h6>
            <h4>{{ activeUsers }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-warning">
            <i class="fas fa-car"></i>
          </div>
          <div class="stats-content">
            <h6>Current Parked</h6>
            <h4>{{ currentParked }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-info">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="stats-content">
            <h6>Avg Bookings</h6>
            <h4>{{ avgBookings }}</h4>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-4">
            <div class="search-box">
              <i class="fas fa-search search-icon"></i>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Search users..."
              >
            </div>
          </div>
          <div class="col-md-2">
            <select v-model="filterStatus" class="form-select">
              <option value="">All Users</option>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
              <option value="parked">Currently Parked</option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="sortBy" class="form-select">
              <option value="name">Sort by Name</option>
              <option value="email">Sort by Email</option>
              <option value="bookings">Sort by Bookings</option>
              <option value="recent">Sort by Recent Activity</option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="itemsPerPage" class="form-select">
              <option :value="10">10 per page</option>
              <option :value="25">25 per page</option>
              <option :value="50">50 per page</option>
              <option :value="100">100 per page</option>
            </select>
          </div>
          <div class="col-md-2">
            <div class="view-toggle">
              <div class="btn-group w-100" role="group">
                <input
                  type="radio"
                  class="btn-check"
                  id="tableView"
                  :checked="viewMode === 'table'"
                  @change="viewMode = 'table'"
                >
                <label class="btn btn-outline-primary" for="tableView">
                  <i class="fas fa-table"></i>
                </label>
                <input
                  type="radio"
                  class="btn-check"
                  id="cardView"
                  :checked="viewMode === 'cards'"
                  @change="viewMode = 'cards'"
                >
                <label class="btn btn-outline-primary" for="cardView">
                  <i class="fas fa-th-large"></i>
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading users...</p>
    </div>
    
    <div v-else-if="viewMode === 'table'" class="table-view">
      <div v-if="paginatedUsers.length === 0" class="empty-state">
        <i class="fas fa-users text-muted"></i>
        <h5>No users found</h5>
        <p class="text-muted">Try adjusting your search criteria</p>
      </div>
      <div v-else class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>User</th>
              <th>Contact</th>
              <th>Location</th>
              <th>Activity</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id">
              <td>
                <div class="user-info">
                  <div class="user-avatar">
                    <i class="fas fa-user-circle"></i>
                  </div>
                  <div class="user-details">
                    <div class="user-name">{{ user.fullname }}</div>
                    <div class="username">@{{ user.username }}</div>
                  </div>
                </div>
              </td>
              <td>
                <div class="contact-info">
                  <div class="email">
                    <i class="fas fa-envelope me-1"></i>
                    {{ user.email }}
                  </div>
                  <div class="location">
                    <i class="fas fa-map-marker-alt me-1"></i>
                    {{ user.pin_code }}
                  </div>
                </div>
              </td>
              <td>
                <div class="location-info">
                  <small class="text-muted">{{ user.address }}</small>
                </div>
              </td>
              <td>
                <div class="activity-info">
                  <div class="bookings">
                    <strong>{{ user.total_reservations }}</strong> bookings
                  </div>
                  <div class="active-status">
                    <span v-if="user.active_reservations > 0" class="badge bg-success">
                      {{ user.active_reservations }} active
                    </span>
                    <span v-else class="text-muted">No active bookings</span>
                  </div>
                </div>
              </td>
              <td>
                <span class="status-badge" :class="getUserStatusClass(user)">
                  <i class="fas" :class="getUserStatusIcon(user)"></i>
                  {{ getUserStatusText(user) }}
                </span>
              </td>
              <td>
                <div class="action-buttons">
                  <button
                    class="btn btn-sm btn-outline-primary me-1"
                    @click="viewUserDetails(user)"
                    title="View Details"
                  >
                    <i class="fas fa-eye"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-else-if="viewMode === 'cards'" class="cards-view">
      <div v-if="paginatedUsers.length === 0" class="empty-state">
        <i class="fas fa-users text-muted"></i>
        <h5>No users found</h5>
        <p class="text-muted">Try adjusting your search criteria</p>
      </div>
      <div v-else class="row">
        <div v-for="user in paginatedUsers" :key="user.id" class="col-md-6 col-lg-4 mb-4">
          <div class="user-card">
            <div class="card-header">
              <div class="d-flex align-items-center">
                <div class="user-avatar-large me-3">
                  <i class="fas fa-user-circle"></i>
                </div>
                <div class="flex-grow-1">
                  <h6 class="user-name">{{ user.fullname }}</h6>
                  <p class="username">@{{ user.username }}</p>
                  <span class="status-badge" :class="getUserStatusClass(user)">
                    <i class="fas" :class="getUserStatusIcon(user)"></i>
                    {{ getUserStatusText(user) }}
                  </span>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="contact-section mb-3">
                <div class="contact-item">
                  <i class="fas fa-envelope text-muted me-2"></i>
                  <span class="text-truncate">{{ user.email }}</span>
                </div>
                <div class="contact-item">
                  <i class="fas fa-map-marker-alt text-muted me-2"></i>
                  <span>{{ user.pin_code }}</span>
                </div>
              </div>
              <div class="stats-section">
                <div class="row text-center">
                  <div class="col-6">
                    <div class="stat-item">
                      <div class="stat-number">{{ user.total_reservations }}</div>
                      <div class="stat-label">Total Bookings</div>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="stat-item">
                      <div class="stat-number">{{ user.active_reservations }}</div>
                      <div class="stat-label">Active</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="action-buttons mt-1">
                <button
                  class="btn btn-sm btn-primary me-1"
                  @click="viewUserDetails(user)"
                >
                  <i class="fas fa-eye me-1"></i>Details
                </button>
                <button
                  class="btn btn-sm btn-outline-primary"
                  @click="sendMessage(user)"
                >
                  <i class="fas fa-envelope me-1"></i>Message
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage = 1">
              <i class="fas fa-angle-double-left"></i>
            </a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage--">
              <i class="fas fa-angle-left"></i>
            </a>
          </li>
          <li
            v-for="page in visiblePages"
            :key="page"
            class="page-item"
            :class="{ active: page === currentPage }"
          >
            <a class="page-link" href="#" @click.prevent="currentPage = page">
              {{ page }}
            </a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" href="#" @click.prevent="currentPage++">
              <i class="fas fa-angle-right"></i>
            </a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" href="#" @click.prevent="currentPage = totalPages">
              <i class="fas fa-angle-double-right"></i>
            </a>
          </li>
        </ul>
      </nav>
    </div>
    
    <div v-if="selectedUser" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user me-2"></i>
              User Details - {{ selectedUser.fullname }}
            </h5>
            <button type="button" class="btn-close" @click="selectedUser = null"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-primary">Personal Information</h6>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Full Name</label>
                    <span>{{ selectedUser.fullname }}</span>
                  </div>
                  <div class="detail-item">
                    <label>Username</label>
                    <span>@{{ selectedUser.username }}</span>
                  </div>
                  <div class="detail-item">
                    <label>Email</label>
                    <span>{{ selectedUser.email }}</span>
                  </div>
                  <div class="detail-item">
                    <label>PIN Code</label>
                    <span>{{ selectedUser.pin_code }}</span>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <h6 class="text-primary">Activity Summary</h6>
                <div class="activity-summary">
                  <div class="summary-item">
                    <div class="summary-icon bg-primary">
                      <i class="fas fa-calendar"></i>
                    </div>
                    <div class="summary-content">
                      <div class="summary-number">{{ selectedUser.total_reservations }}</div>
                      <div class="summary-label">Total Bookings</div>
                    </div>
                  </div>
                  <div class="summary-item">
                    <div class="summary-icon bg-success">
                      <i class="fas fa-car"></i>
                    </div>
                    <div class="summary-content">
                      <div class="summary-number">{{ selectedUser.active_reservations }}</div>
                      <div class="summary-label">Active Bookings</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-4">
              <h6 class="text-primary">Address</h6>
              <p class="address-text">{{ selectedUser.address }}</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedUser = null">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="selectedUser" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
export default {
  name: 'UserList',
  setup() {
    const adminStore = useAdminStore()
    const isLoading = ref(false)
    const searchQuery = ref('')
    const filterStatus = ref('')
    const sortBy = ref('name')
    const viewMode = ref('table')
    const itemsPerPage = ref(10)
    const currentPage = ref(1)
    const selectedUser = ref(null)
    const totalUsers = computed(() => adminStore.users.length)
    const activeUsers = computed(() =>
      adminStore.users.filter(user => user.total_reservations > 0).length
    )
    const currentParked = computed(() =>
      adminStore.users.filter(user => user.active_reservations > 0).length
    )
    const avgBookings = computed(() => {
      const total = adminStore.users.reduce((sum, user) => sum + user.total_reservations, 0)
      return totalUsers.value > 0 ? Math.round(total / totalUsers.value) : 0
    })
    const filteredUsers = computed(() => {
      let users = [...adminStore.users]
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        users = users.filter(user =>
          user.fullname.toLowerCase().includes(query) ||
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query) ||
          user.pin_code.includes(query)
        )
      }
      if (filterStatus.value) {
        users = users.filter(user => {
          switch (filterStatus.value) {
            case 'active':
              return user.total_reservations > 0
            case 'inactive':
              return user.total_reservations === 0
            case 'parked':
              return user.active_reservations > 0
            default:
              return true
          }
        })
      }
      users.sort((a, b) => {
        switch (sortBy.value) {
          case 'name':
            return a.fullname.localeCompare(b.fullname)
          case 'email':
            return a.email.localeCompare(b.email)
          case 'bookings':
            return b.total_reservations - a.total_reservations
          case 'recent':
            return b.id - a.id
          default:
            return 0
        }
      })
      return users
    })
    const totalPages = computed(() =>
      Math.ceil(filteredUsers.value.length / itemsPerPage.value)
    )
    const paginatedUsers = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      const end = start + itemsPerPage.value
      return filteredUsers.value.slice(start, end)
    })
    const visiblePages = computed(() => {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2))
      let end = Math.min(totalPages.value, start + maxVisible - 1)
      if (end - start < maxVisible - 1) {
        start = Math.max(1, end - maxVisible + 1)
      }
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    })
    const getUserStatusClass = (user) => {
      if (user.active_reservations > 0) return 'status-active'
      if (user.total_reservations > 0) return 'status-regular'
      return 'status-new'
    }
    const getUserStatusIcon = (user) => {
      if (user.active_reservations > 0) return 'fa-car'
      if (user.total_reservations > 0) return 'fa-check'
      return 'fa-user-plus'
    }
    const getUserStatusText = (user) => {
      if (user.active_reservations > 0) return 'Currently Parked'
      if (user.total_reservations > 0) return 'Regular User'
      return 'New User'
    }
    const viewUserDetails = (user) => {
      selectedUser.value = user
    }
    const sendMessage = (user) => {
      console.log('Send message to:', user.email)
    }
    const exportUserData = (user) => {
      console.log('Export data for:', user.username)
    }
    const viewUserActivity = (user) => {
      console.log('View activity for:', user.username)
    }
    const suspendUser = (user) => {
      if (confirm(`Are you sure you want to suspend ${user.fullname}?`)) {
        console.log('Suspend user:', user.username)
      }
    }
    const exportUsers = () => {
      console.log('Export all users')
    }
    const refreshData = async () => {
      await loadData()
    }
    const loadData = async () => {
      isLoading.value = true
      try {
        await adminStore.fetchUsers()
      } catch (error) {
        console.error('Error loading users:', error)
      } finally {
        isLoading.value = false
      }
    }
    onMounted(() => {
      loadData()
    })
    return {
      isLoading,
      searchQuery,
      filterStatus,
      sortBy,
      viewMode,
      itemsPerPage,
      currentPage,
      selectedUser,
      totalUsers,
      activeUsers,
      currentParked,
      avgBookings,
      paginatedUsers,
      totalPages,
      visiblePages,
      getUserStatusClass,
      getUserStatusIcon,
      getUserStatusText,
      viewUserDetails,
      sendMessage,
      exportUserData,
      viewUserActivity,
      suspendUser,
      exportUsers,
      refreshData
    }
  }
}
</script>
<style scoped>
.user-list {
  padding: 1rem;
}
.text-primary {
  color: #99ebff !important;
}
.text-muted {
  color: #00cccc !important;
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-primary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-primary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.stats-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.stats-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  margin-right: 1rem;
}
.stats-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.stats-content h6 {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}
.stats-content h4 {
  color: var(--primary-color);
  font-weight: 700;
  margin: 0;
}
.search-box {
  position: relative;
}
.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  z-index: 2;
}
.search-box .form-control {
  padding-left: 2.5rem;
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 8px;
}
.table {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.table th {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  border: none;
  padding: 1rem;
  font-weight: 600;
}
.table td {
  padding: 1rem;
  border-bottom: 1px solid rgba(138, 184, 254, 0.1);
  vertical-align: middle;
}
.user-info {
  display: flex;
  align-items: center;
}
.user-avatar {
  font-size: 2rem;
  color: var(--secondary-color);
  margin-right: 0.75rem;
}
.user-avatar-large {
  font-size: 3rem;
  color: var(--secondary-color);
}
.user-name {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.username {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0;
}
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}
.status-active {
  background-color: #d4edda;
  color: #155724;
}
.status-regular {
  background-color: #cce5ff;
  color: var(--primary-color);
}
.status-new {
  background-color: #fff3cd;
  color: #856404;
}
.user-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}
.user-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 1, 51, 0.15);
}
.user-card .card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: none;
  padding: 1.25rem;
}
.contact-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}
.stat-item {
  padding: 0.5rem;
}
.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}
.stat-label {
  font-size: 0.8rem;
  color: #6c757d;
}
.pagination .page-link {
  color: var(--secondary-color);
  border-color: rgba(138, 184, 254, 0.3);
  border-radius: 8px;
  margin: 0 2px;
}
.pagination .page-item.active .page-link {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.pagination .page-link:hover {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: var(--secondary-color);
}
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}
.empty-state i {
  font-size: 4rem;
  margin-bottom: 1rem;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}
.detail-item label {
  font-weight: 600;
  color: #6c757d;
  margin: 0;
}
.summary-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.summary-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 0.75rem;
}
.summary-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.summary-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--primary-color);
}
.summary-label {
  font-size: 0.9rem;
  color: #6c757d;
}
.address-text {
  background: rgba(138, 184, 254, 0.1);
  padding: 1rem;
  border-radius: 8px;
  margin: 0;
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
@media (max-width: 768px) {
  .stats-card {
    margin-bottom: 0.5rem;
  }
  .user-info {
    flex-direction: column;
    align-items: flex-start;
  }
  .user-avatar {
    margin-bottom: 0.5rem;
  }
  .action-buttons .btn {
    margin-bottom: 0.25rem;
  }
  .table-responsive {
    font-size: 0.85rem;
  }
}
</style>