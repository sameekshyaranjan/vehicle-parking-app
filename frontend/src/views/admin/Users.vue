<template>
  <div class="admin-users">
    <div class="main-content">
      <UserList
        :filter-tab="activeTab"
        @user-selected="handleUserSelected"
        @user-edited="handleUserEdited"
        @user-suspended="handleUserSuspended"
        @send-message="handleSendMessage"
      />
    </div>
    <div v-if="selectedUser" class="modal d-block">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user me-2"></i>
              User Profile - {{ selectedUser.fullname }}
            </h5>
            <button type="button" class="btn-close" @click="closeUserModal"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-4">
                <div class="user-profile-card">
                  <div class="profile-header">
                    <div class="profile-avatar">
                      <i class="fas fa-user-circle"></i>
                    </div>
                    <h5>{{ selectedUser.fullname }}</h5>
                    <p class="text-muted">@{{ selectedUser.username }}</p>
                    <span class="status-badge" :class="getUserStatusClass(selectedUser)">
                      {{ getUserStatusText(selectedUser) }}
                    </span>
                  </div>
                  <div class="profile-details">
                    <div class="detail-item">
                      <label>Email</label>
                      <span>{{ selectedUser.email }}</span>
                    </div>
                    <div class="detail-item">
                      <label>Phone</label>
                      <span>{{ selectedUser.phone || 'Not provided' }}</span>
                    </div>
                    <div class="detail-item">
                      <label>Address</label>
                      <span>{{ selectedUser.address }}</span>
                    </div>
                    <div class="detail-item">
                      <label>PIN Code</label>
                      <span>{{ selectedUser.pin_code }}</span>
                    </div>
                    <div class="detail-item">
                      <label>Joined</label>
                      <span>{{ formatDate(selectedUser.created_at) }}</span>
                    </div>
                  </div>
                  <div class="profile-actions">
                    <button class="btn btn-primary btn-sm w-100 mb-2" @click="sendDirectMessage">
                      <i class="fas fa-envelope me-1"></i>Send Message
                    </button>
                    <button class="btn btn-outline-warning btn-sm w-100 mb-2" @click="suspendUser">
                      <i class="fas fa-ban me-1"></i>Suspend User
                    </button>
                    <button class="btn btn-outline-danger btn-sm w-100" @click="deleteUser">
                      <i class="fas fa-trash me-1"></i>Delete User
                    </button>
                  </div>
                </div>
              </div>
              <div class="col-md-8">
                <div class="user-analytics">
                  <div class="stats-overview mb-4">
                    <div class="row">
                      <div class="col-6 col-md-3">
                        <div class="mini-stat">
                          <h4>{{ selectedUser.total_bookings || 0 }}</h4>
                          <small>Total Bookings</small>
                        </div>
                      </div>
                      <div class="col-6 col-md-3">
                        <div class="mini-stat">
                          <h4>₹{{ selectedUser.total_spent || 0 }}</h4>
                          <small>Total Spent</small>
                        </div>
                      </div>
                      <div class="col-6 col-md-3">
                        <div class="mini-stat">
                          <h4>{{ selectedUser.active_bookings || 0 }}</h4>
                          <small>Active Bookings</small>
                        </div>
                      </div>
                      <div class="col-6 col-md-3">
                        <div class="mini-stat">
                          <h4>{{ selectedUser.avg_session || 0 }}h</h4>
                          <small>Avg Session</small>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="recent-activity">
                    <h6 class="text-primary mb-3">Recent Activity</h6>
                    <div class="activity-timeline">
                      <div
                        v-for="activity in userActivities"
                        :key="activity.id"
                        class="timeline-item"
                      >
                        <div class="timeline-marker" :class="getActivityMarkerClass(activity.type)">
                          <i class="fas" :class="getActivityIcon(activity.type)"></i>
                        </div>
                        <div class="timeline-content">
                          <div class="activity-description">{{ activity.description }}</div>
                          <div class="activity-time">{{ formatTimeAgo(activity.timestamp) }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="booking-summary mt-4">
                    <h6 class="text-primary mb-3">Booking Summary</h6>
                    <div class="table-responsive">
                      <table class="table table-sm">
                        <thead>
                          <tr>
                            <th>Date</th>
                            <th>Location</th>
                            <th>Duration</th>
                            <th>Cost</th>
                            <th>Status</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="booking in recentBookings" :key="booking.id">
                            <td>{{ formatDate(booking.date) }}</td>
                            <td>{{ booking.location }}</td>
                            <td>{{ booking.duration }}h</td>
                            <td>₹{{ booking.cost }}</td>
                            <td>
                              <span class="badge" :class="getBookingStatusClass(booking.status)">
                                {{ booking.status }}
                              </span>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeUserModal">
              Close
            </button>
            
          </div>
        </div>
      </div>
    </div>
    <div v-if="selectedUser" class="modal-backdrop"></div>
    <div v-if="showCreateUser" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-user-plus me-2"></i>
              Create New User
            </h5>
            <button type="button" class="btn-close" @click="showCreateUser = false"></button>
          </div>
          <div class="modal-body">
            <div class="create-user-form">
              <p class="text-muted">User creation form component would be implemented here.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showCreateUser" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
import UserList from '../../components/admin/UserList.vue'
export default {
  name: 'AdminUsers',
  components: {
    UserList
  },
  setup() {
    const adminStore = useAdminStore()
    const activeTab = ref('all')
    const selectedUser = ref(null)
    const showCreateUser = ref(false)
    const totalUsers = ref(1250)
    const userGrowth = ref(12.5)
    const activeUsers = ref(890)
    const activeGrowth = ref(8.3)
    const newUsersToday = ref(15)
    const newUserChange = ref(-2.1)
    const avgRevenuePerUser = ref(850)
    const revenueGrowth = ref(15.2)
    const userActivities = ref([
      {
        id: 1,
        type: 'booking',
        description: 'Booked parking at Central Mall',
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000)
      },
      {
        id: 2,
        type: 'payment',
        description: 'Payment completed: ₹150',
        timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000)
      },
      {
        id: 3,
        type: 'release',
        description: 'Released parking spot',
        timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000)
      }
    ])
    const recentBookings = ref([
      { id: 1, date: new Date(), location: 'Central Mall', duration: 3, cost: 150, status: 'Completed' },
      { id: 2, date: new Date(), location: 'Office Complex', duration: 8, cost: 400, status: 'Active' },
      { id: 3, date: new Date(), location: 'Metro Station', duration: 2, cost: 100, status: 'Completed' }
    ])
    const inactiveUsers = computed(() => totalUsers.value - activeUsers.value)
    const premiumUsers = computed(() => Math.floor(totalUsers.value * 0.15))
    const setActiveTab = (tab) => {
      activeTab.value = tab
    }
    const handleUserSelected = (user) => {
      selectedUser.value = user
    }
    const handleUserEdited = (user) => {
      console.log('Edit user:', user)
    }
    const handleUserSuspended = (user) => {
      console.log('Suspend user:', user)
    }
    const handleSendMessage = (user) => {
      console.log('Send message to user:', user)
    }
    const closeUserModal = () => {
      selectedUser.value = null
    }
    const getUserStatusClass = (user) => {
      return user.is_active ? 'status-active' : 'status-inactive'
    }
    const getUserStatusText = (user) => {
      return user.is_active ? 'Active' : 'Inactive'
    }
    const getActivityMarkerClass = (type) => {
      const classes = {
        booking: 'marker-booking',
        payment: 'marker-payment',
        release: 'marker-release'
      }
      return classes[type] || 'marker-default'
    }
    const getActivityIcon = (type) => {
      const icons = {
        booking: 'fa-calendar-plus',
        payment: 'fa-rupee-sign',
        release: 'fa-sign-out-alt'
      }
      return icons[type] || 'fa-info-circle'
    }
    const getBookingStatusClass = (status) => {
      const classes = {
        'Completed': 'bg-success',
        'Active': 'bg-primary',
        'Cancelled': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    }
    const formatDate = (date) => {
      return new Date(date).toLocaleDateString('en-IN')
    }
    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const diffMs = now - new Date(timestamp)
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      if (diffHours < 1) return 'Just now'
      if (diffHours < 24) return `${diffHours}h ago`
      const diffDays = Math.floor(diffHours / 24)
      return `${diffDays}d ago`
    }
    const exportUsers = () => {
      console.log('Exporting users data...')
    }
    const sendBulkNotification = () => {
      console.log('Sending bulk notification...')
    }
    const sendDirectMessage = () => {
      console.log('Send direct message to:', selectedUser.value?.username)
    }
    const suspendUser = () => {
      if (confirm(`Are you sure you want to suspend ${selectedUser.value?.fullname}?`)) {
        console.log('Suspending user:', selectedUser.value?.username)
      }
    }
    const deleteUser = () => {
      if (confirm(`Are you sure you want to delete ${selectedUser.value?.fullname}? This action cannot be undone.`)) {
        console.log('Deleting user:', selectedUser.value?.username)
      }
    }
    const exportUserData = () => {
      console.log('Exporting data for user:', selectedUser.value?.username)
    }
    onMounted(() => {
      adminStore.fetchUsers()
    })
    return {
      activeTab,
      selectedUser,
      showCreateUser,
      totalUsers,
      userGrowth,
      activeUsers,
      activeGrowth,
      newUsersToday,
      newUserChange,
      avgRevenuePerUser,
      revenueGrowth,
      inactiveUsers,
      premiumUsers,
      userActivities,
      recentBookings,
      setActiveTab,
      handleUserSelected,
      handleUserEdited,
      handleUserSuspended,
      handleSendMessage,
      closeUserModal,
      getUserStatusClass,
      getUserStatusText,
      getActivityMarkerClass,
      getActivityIcon,
      getBookingStatusClass,
      formatDate,
      formatTimeAgo,
      exportUsers,
      sendBulkNotification,
      sendDirectMessage,
      suspendUser,
      deleteUser,
      exportUserData
    }
  }
}
</script>
<style scoped>
.admin-users {
  padding: 1.5rem;
}
.page-title {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.page-subtitle {
  color: #6c757d;
  margin: 0;
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-primary, .btn-outline-success {
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-primary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}
.btn-outline-primary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.stat-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}
.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 1, 51, 0.15);
}
.stat-icon {
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
.stat-card.total-users .stat-icon {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.stat-card.active-users .stat-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}
.stat-card.new-users .stat-icon {
  background: linear-gradient(135deg, #fd7e14, #f8b500);
}
.stat-card.revenue-per-user .stat-icon {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}
.stat-content h3 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
  font-size: 1.75rem;
}
.stat-content p {
  color: #6c757d;
  margin-bottom: 0.5rem;
}
.stat-trend {
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}
.stat-trend.positive {
  color: #28a745;
}
.stat-trend.negative {
  color: #dc3545;
}
.stat-trend.neutral {
  color: #6c757d;
}
.filter-tabs .nav-pills .nav-link {
  background: transparent;
  border: 2px solid rgba(138, 184, 254, 0.3);
  color: var(--secondary-color);
  border-radius: 25px;
  margin-right: 0.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
}
.filter-tabs .nav-pills .nav-link:hover {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: var(--secondary-color);
}
.filter-tabs .nav-pills .nav-link.active {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border-color: var(--secondary-color);
  color: white;
}
.user-profile-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  height: fit-content;
}
.profile-header {
  text-align: center;
  margin-bottom: 2rem;
}
.profile-avatar {
  font-size: 4rem;
  color: var(--secondary-color);
  margin-bottom: 1rem;
}
.profile-header h5 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
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
.status-inactive {
  background-color: #f8d7da;
  color: #721c24;
}
.profile-details {
  margin-bottom: 2rem;
}
.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(138, 184, 254, 0.1);
}
.detail-item:last-child {
  border-bottom: none;
}
.detail-item label {
  font-weight: 600;
  color: #6c757d;
  margin: 0;
}
.detail-item span {
  color: var(--primary-color);
  font-weight: 500;
}
.mini-stat {
  text-align: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
  margin-bottom: 1rem;
}
.mini-stat h4 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.mini-stat small {
  color: #6c757d;
}
.activity-timeline {
  position: relative;
  padding-left: 2rem;
}
.timeline-item {
  position: relative;
  padding-bottom: 1.5rem;
}
.timeline-item::before {
  content: '';
  position: absolute;
  left: -2rem;
  top: 2rem;
  width: 2px;
  height: calc(100% - 1rem);
  background: rgba(138, 184, 254, 0.3);
}
.timeline-item:last-child::before {
  display: none;
}
.timeline-marker {
  position: absolute;
  left: -2.5rem;
  top: 0;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.8rem;
}
.marker-booking {
  background: var(--secondary-color);
}
.marker-payment {
  background: #28a745;
}
.marker-release {
  background: #fd7e14;
}
.timeline-content {
  margin-left: 0.5rem;
}
.activity-description {
  color: var(--primary-color);
  font-weight: 500;
  margin-bottom: 0.25rem;
}
.activity-time {
  color: #6c757d;
  font-size: 0.85rem;
}
.table {
  background: white;
  border-radius: 10px;
  overflow: hidden;
}
.table th {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: none;
  font-weight: 600;
  color: var(--primary-color);
}
.table td {
  border-bottom: 1px solid rgba(138, 184, 254, 0.1);
  vertical-align: middle;
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
.modal-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  border-radius: 15px 15px 0 0 !important;
}
@media (max-width: 768px) {
  .admin-users {
    padding: 1rem;
  }
  .header-actions {
    margin-top: 1rem;
  }
  .filter-tabs .nav-pills {
    flex-wrap: wrap;
  }
  .profile-details {
    margin-bottom: 1rem;
  }
}
</style>