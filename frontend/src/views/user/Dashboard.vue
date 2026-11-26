<template>
  <div class="user-dashboard">
    <div class="dashboard-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-8">
          <div class="welcome-section">
            <h2 class="welcome-title">
              Welcome back, {{ authStore.userName }}! 👋
            </h2>
            <p class="welcome-subtitle">
              {{ getGreetingMessage() }} Ready to find your perfect parking spot?
            </p>
          </div>
        </div>
        <div class="col-md-4 text-md-end">
          <div class="quick-actions">
            <router-link to="/user/reserve-parking" class="btn btn-primary">
              <i class="fas fa-plus me-1"></i>Reserve Parking
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeReservation" class="active-booking-alert mb-4">
      <div class="alert alert-info">
        <div class="row align-items-center">
          <div class="col-md-8">
            <div class="d-flex align-items-center">
              <i class="fas fa-car fa-2x me-3 text-primary"></i>
              <div>
                <h6 class="alert-heading mb-1">You have an active parking session</h6>
                <p class="mb-1">
                  <strong>{{ activeReservation.lot_name }}</strong> -
                  Spot #{{ activeReservation.spot_number }}
                </p>
                <small class="text-muted">
                  Parked since {{ formatDateTime(activeReservation.parking_timestamp) }}
                </small>
              </div>
            </div>
          </div>
          <div class="col-md-4 text-md-end">
            <button class="btn btn-warning me-2" @click="extendBooking(activeReservation)">
              <i class="fas fa-clock me-1"></i>Extend
            </button>
            <button class="btn btn-success" @click="releaseSpot(activeReservation)">
              <i class="fas fa-sign-out-alt me-1"></i>Release
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="stats-section mb-4">
      <div class="row">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card total-bookings">
            <div class="stat-icon">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div class="stat-content">
              <h3>{{ userStats.totalBookings }}</h3>
              <p>Total Bookings</p>
              <small class="text-success">
                <i class="fas fa-arrow-up me-1"></i>
                +{{ userStats.bookingGrowth }}% this month
              </small>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card hours-parked">
            <div class="stat-icon">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-content">
              <h3>{{ userStats.totalHours }}h</h3>
              <p>Hours Parked</p>
              <small class="text-info">
                <i class="fas fa-clock me-1"></i>
                Avg {{ userStats.avgDuration }}h per session
              </small>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card money-spent">
            <div class="stat-icon">
              <i class="fas fa-rupee-sign"></i>
            </div>
            <div class="stat-content">
              <h3>₹{{ userStats.totalSpent }}</h3>
              <p>Total Spent</p>
              <small class="text-warning">
                <i class="fas fa-chart-line me-1"></i>
                ₹{{ userStats.avgCost }} avg per booking
              </small>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card savings">
            <div class="stat-icon">
              <i class="fas fa-piggy-bank"></i>
            </div>
            <div class="stat-content">
              <h3>₹{{ userStats.totalSavings }}</h3>
              <p>Total Savings</p>
              <small class="text-success">
                <i class="fas fa-percentage me-1"></i>
                {{ userStats.savingsRate }}% saved vs street parking
              </small>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-lg-8">
        <div class="card mb-4">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-bolt me-2"></i>Quick Reserve
            </h6>
          </div>
          <div class="card-body">
            <div class="quick-reserve">
              <div class="row">
                <div class="col-md-8">
                  <div class="search-section">
                    <label class="form-label">Where would you like to park?</label>
                    <div class="location-search">
                      <div class="input-group">
                        <span class="input-group-text">
                          <i class="fas fa-map-marker-alt"></i>
                        </span>
                        <input
                          v-model="quickSearch.location"
                          type="text"
                          class="form-control"
                          placeholder="Enter location, area, or landmark..."
                          @keyup.enter="searchLocations"
                        >
                        <button class="btn btn-primary" @click="searchLocations">
                          <i class="fas fa-search"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="datetime-section mt-3">
                    <div class="row">
                      <div class="col-6">
                        <label class="form-label">Date</label>
                        <input
                          v-model="quickSearch.date"
                          type="date"
                          class="form-control"
                          :min="today"
                        >
                      </div>
                      <div class="col-6">
                        <label class="form-label">Time</label>
                        <input
                          v-model="quickSearch.time"
                          type="time"
                          class="form-control"
                        >
                      </div>
                    </div>
                  </div>
                </div>
                <div class="col-md-4 text-center">
                  <div class="quick-stats">
                    <div class="quick-stat-item">
                      <h4>{{ nearbyLots }}</h4>
                      <small>Nearby Locations</small>
                    </div>
                    <div class="quick-stat-item">
                      <h4>{{ availableSpots }}</h4>
                      <small>Available Spots</small>
                    </div>
                    <button class="btn btn-success w-100 mt-3" @click="goToReserve">
                      <i class="fas fa-search me-1"></i>Find Parking
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <h6 class="mb-0">
                <i class="fas fa-history me-2"></i>Recent Bookings
              </h6>
              <router-link to="/user/my-bookings" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
          </div>
          <div class="card-body">
            <div v-if="recentBookings.length === 0" class="empty-state text-center py-4">
              <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
              <h6>No Recent Bookings</h6>
              <p class="text-muted">Start by making your first parking reservation!</p>
              <router-link to="/user/reserve-parking" class="btn btn-primary">
                <i class="fas fa-plus me-1"></i>Reserve Now
              </router-link>
            </div>
            <div v-else class="recent-bookings-list">
              <div
                v-for="booking in recentBookings"
                :key="booking.id"
                class="booking-item"
              >
                <div class="booking-info">
                  <div class="booking-location">
                    <h6>{{ booking.lot_name }}</h6>
                    <small class="text-muted">Spot #{{ booking.spot_number }}</small>
                  </div>
                  <div class="booking-details">
                    <span class="booking-date">{{ formatDate(booking.date) }}</span>
                    <span class="booking-cost">₹{{ booking.cost }}</span>
                  </div>
                </div>
                <div class="booking-status">
                  <span class="badge" :class="getStatusClass(booking.status)">
                    {{ booking.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="col-lg-4">
        <div class="card mb-4">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-heart me-2"></i>Favorite Locations
            </h6>
          </div>
          <div class="card-body">
            <div class="favorite-locations">
              <div
                v-for="location in favoriteLocations"
                :key="location.id"
                class="favorite-item"
              >
                <div class="favorite-info">
                  <h6>{{ location.name }}</h6>
                  <small class="text-muted">{{ location.visits }} visits</small>
                </div>
                <div class="favorite-actions">
                  <button
                    class="btn btn-sm btn-primary"
                    @click="quickBookFavorite(location)"
                  >
                    <i class="fas fa-bolt"></i>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card mb-4">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-bell me-2"></i>Notifications
            </h6>
          </div>
          <div class="card-body">
            <div class="notifications-list">
              <div
                v-for="notification in notifications"
                :key="notification.id"
                class="notification-item"
                :class="{ 'unread': !notification.read }"
              >
                <div class="notification-icon" :class="getNotificationClass(notification.type)">
                  <i class="fas" :class="getNotificationIcon(notification.type)"></i>
                </div>
                <div class="notification-content">
                  <div class="notification-text">{{ notification.message }}</div>
                  <div class="notification-time">{{ formatTimeAgo(notification.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="card">
          <div class="card-header">
            <h6 class="mb-0">
              <i class="fas fa-rocket me-2"></i>Quick Actions
            </h6>
          </div>
          <div class="card-body">
            <div class="quick-actions-grid">
              <router-link to="/user/reserve-parking" class="action-item">
                <i class="fas fa-plus"></i>
                <span>Reserve Parking</span>
              </router-link>
              <router-link to="/user/my-bookings" class="action-item">
                <i class="fas fa-history"></i>
                <span>My Bookings</span>
              </router-link>
              <router-link to="/user/statistics" class="action-item">
                <i class="fas fa-chart-line"></i>
                <span>View Reports</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showReleaseModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-sign-out-alt me-2"></i>Release Parking Spot
            </h5>
            <button type="button" class="btn-close" @click="showReleaseModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Please rate your parking experience at <strong>{{ releasingBooking?.lot_name }}</strong> before releasing the spot.</p>
            <div class="rating-section mt-3">
              <label class="form-label">Your Rating:</label>
              <div class="star-rating">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  class="star-btn"
                  :class="{ active: star <= releaseRating }"
                  @click="releaseRating = star"
                >
                  <i class="fas fa-star"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="showReleaseModal = false">
              Cancel
            </button>
            <button type="button" class="btn btn-success" @click="confirmRelease">
              <i class="fas fa-check me-1"></i>Confirm Release
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useUserStore } from '@/store/modules/user'
export default {
  name: 'UserDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const userStore = useUserStore()
    const showReleaseModal = ref(false)
    const releasingBooking = ref(null)
    const releaseRating = ref(5)
    const quickSearch = reactive({
      location: '',
      date: '',
      time: ''
    })
    const userStats = computed(() => userStore.userStats)
    const activeReservation = computed(() => userStore.activeReservation)
    const recentBookings = computed(() => userStore.recentBookings)
    const favoriteLocations = computed(() => userStore.favoriteLocations)
    const nearbyLots = computed(() => userStore.nearbyLots)
    const availableSpots = computed(() => userStore.availableSpots)
    const notifications = computed(() => userStore.notifications)
    const isLoading = computed(() => userStore.isLoading)
    const error = computed(() => userStore.error)
    const today = computed(() => new Date().toISOString().split('T')[0])
    const getGreetingMessage = () => {
      const hour = new Date().getHours()
      if (hour < 12) return 'Good morning!'
      if (hour < 17) return 'Good afternoon!'
      return 'Good evening!'
    }
    const formatDateTime = (dateString) => {
      return new Date(dateString).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('en-IN', {
        month: 'short',
        day: 'numeric'
      })
    }
    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const diffMs = now - new Date(timestamp)
      const diffMins = Math.floor(diffMs / 60000)
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      const diffHours = Math.floor(diffMins / 60)
      if (diffHours < 24) return `${diffHours}h ago`
      const diffDays = Math.floor(diffHours / 24)
      return `${diffDays}d ago`
    }
    const getStatusClass = (status) => {
      const classes = {
        'Completed': 'bg-success',
        'Active': 'bg-primary',
        'Cancelled': 'bg-danger'
      }
      return classes[status] || 'bg-secondary'
    }
    const getNotificationClass = (type) => {
      const classes = {
        success: 'notification-success',
        info: 'notification-info',
        warning: 'notification-warning',
        error: 'notification-error'
      }
      return classes[type] || 'notification-info'
    }
    const getNotificationIcon = (type) => {
      const icons = {
        success: 'fa-check-circle',
        info: 'fa-info-circle',
        warning: 'fa-exclamation-triangle',
        error: 'fa-times-circle'
      }
      return icons[type] || 'fa-info-circle'
    }
    const searchLocations = async () => {
      try {
        await userStore.searchLocations({
          location: quickSearch.location,
          date: quickSearch.date,
          time: quickSearch.time
        })
        router.push({
          path: '/user/reserve-parking',
          query: {
            location: quickSearch.location,
            date: quickSearch.date,
            time: quickSearch.time
          }
        })
      } catch (error) {
        console.error('Search error:', error)
      }
    }
    const goToReserve = () => {
      router.push('/user/reserve-parking')
    }
    const quickBookFavorite = async (location) => {
      try {
        const result = await userStore.quickBookFavorite(location)
        router.push({
          path: '/user/reserve-parking',
          query: { locationId: result.locationId }
        })
      } catch (error) {
        console.error('Quick book error:', error)
      }
    }
    const extendBooking = async (booking) => {
      try {
        await userStore.extendBooking(booking.id, 1)
        console.log('Booking extended successfully')
      } catch (error) {
        console.error('Error extending booking:', error)
      }
    }
    const releaseSpot = (booking) => {
      releasingBooking.value = booking
      releaseRating.value = 5
      showReleaseModal.value = true
    }
    const confirmRelease = async () => {
      if (releasingBooking.value) {
        try {
          await userStore.releaseBooking(releasingBooking.value.id, releaseRating.value)
          console.log('Parking spot released successfully')
          showReleaseModal.value = false
          releasingBooking.value = null
        } catch (error) {
          console.error('Error releasing spot:', error)
        }
      }
    }
    const showProfile = () => {
      console.log('Show user profile')
    }
    const markNotificationRead = async (notificationId) => {
      try {
        await userStore.markNotificationRead(notificationId)
      } catch (error) {
        console.error('Error marking notification as read:', error)
      }
    }
    onMounted(async () => {
      quickSearch.date = today.value
      quickSearch.time = new Date().toTimeString().slice(0, 5)
      try {
        await userStore.fetchDashboardData()
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      }
    })
    return {
      userStats,
      activeReservation,
      recentBookings,
      favoriteLocations,
      nearbyLots,
      availableSpots,
      notifications,
      isLoading,
      error,
      quickSearch,
      authStore,
      today,
      getGreetingMessage,
      formatDateTime,
      formatDate,
      formatTimeAgo,
      getStatusClass,
      getNotificationClass,
      getNotificationIcon,
      searchLocations,
      goToReserve,
      quickBookFavorite,
      extendBooking,
      releaseSpot,
      showProfile,
      markNotificationRead,
      showReleaseModal,
      releasingBooking,
      releaseRating,
      confirmRelease,
    }
  }
}
</script>
<style scoped>
.user-dashboard {
  padding: 1.5rem;
}
.welcome-title {
  color: white;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.welcome-subtitle {
  color: #6c757d;
  margin: 0;
  font-size: 1.1rem;
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.active-booking-alert .alert {
  background: linear-gradient(135deg,whitesmoke, rgba(255, 255, 255, 0.9));
  border: 2px solid var(--text-accent);
  border-radius: 15px;
}
.stat-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
  height: 100%;
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
.stat-card.total-bookings .stat-icon { background: linear-gradient(135deg, var(--secondary-color), var(--primary-color)); }
.stat-card.hours-parked .stat-icon { background: linear-gradient(135deg, #28a745, #20c997); }
.stat-card.money-spent .stat-icon { background: linear-gradient(135deg, #fd7e14, #f8b500); }
.stat-card.savings .stat-icon { background: linear-gradient(135deg, #6f42c1, #e83e8c); }
.stat-content h3 { color: var(--primary-color); font-weight: 700; margin-bottom: 0.25rem; font-size: 1.75rem; }
.stat-content p { color: #6c757d; margin-bottom: 0.5rem; }
.stat-content small { font-size: 0.85rem; font-weight: 500; }
.card { border: none; border-radius: 15px; box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1); }
.card-header { background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9)); border-radius: 15px 15px 0 0 !important; padding: 1.25rem; }
.card-header h6 { color: var(--primary-color); font-weight: 600; margin: 0; }
.form-control { border: 2px solid rgba(138, 184, 254, 0.3); border-radius: 8px; transition: all 0.3s ease; }
.form-control:focus { border-color: var(--secondary-color); box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25); }
.quick-stats { padding: 1rem; background: rgba(138, 184, 254, 0.05); border-radius: 10px; }
.quick-stat-item { text-align: center; margin-bottom: 1rem; }
.quick-stat-item h4 { color: var(--primary-color); font-weight: 700; margin-bottom: 0.25rem; }
.quick-stat-item small { color: #6c757d; }
.booking-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: rgba(138, 184, 254, 0.05); border-radius: 10px; margin-bottom: 1rem; }
.booking-item:last-child { margin-bottom: 0; }
.booking-location h6 { color: var(--primary-color); font-weight: 600; margin-bottom: 0.25rem; }
.booking-details { display: flex; gap: 1rem; margin-top: 0.5rem; }
.booking-date, .booking-cost { font-size: 0.9rem; color: #6c757d; font-weight: 500; }
.booking-cost { color: var(--secondary-color); font-weight: 600; }
.favorite-item { display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: rgba(138, 184, 254, 0.05); border-radius: 10px; margin-bottom: 1rem; }
.favorite-item:last-child { margin-bottom: 0; }
.favorite-info h6 { color: var(--primary-color); font-weight: 600; margin-bottom: 0.25rem; }
.notification-item { display: flex; align-items: flex-start; padding: 1rem; margin-bottom: 1rem; border-radius: 10px; transition: all 0.3s ease; }
.notification-item:last-child { margin-bottom: 0; }
.notification-item.unread { background: rgba(138, 184, 254, 0.1); border-left: 4px solid var(--secondary-color); }
.notification-icon { width: 35px; height: 35px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; margin-right: 0.75rem; font-size: 1rem; }
.notification-success { background: #28a745; }
.notification-info { background: #17a2b8; }
.notification-warning { background: #ffc107; }
.notification-error { background: #dc3545; }
.notification-content { flex: 1; }
.notification-text { color: var(--primary-color); font-weight: 500; margin-bottom: 0.25rem; font-size: 0.9rem; }
.notification-time { color: #6c757d; font-size: 0.8rem; }
.quick-actions-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
.action-item { display: flex; flex-direction: column; align-items: center; padding: 1.5rem 1rem; background: rgba(138, 184, 254, 0.05); border-radius: 10px; text-decoration: none; color: var(--primary-color); transition: all 0.3s ease; border: none; cursor: pointer; }
.action-item:hover { background: rgba(138, 184, 254, 0.1); transform: translateY(-2px); color: var(--secondary-color); }
.action-item i { font-size: 1.5rem; margin-bottom: 0.5rem; }
.action-item span { font-size: 0.9rem; font-weight: 600; text-align: center; }
.empty-state i { color: #dee2e6; }
.rating-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.star-rating {
  display: flex;
  gap: 0.5rem;
}
.star-btn {
  background: none;
  border: none;
  color: #ddd;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.star-btn:hover,
.star-btn.active {
  color: #ffc107;
  transform: scale(1.1);
}
</style>