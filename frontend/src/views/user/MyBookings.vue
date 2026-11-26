<template>
  <div class="my-bookings">
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h2 class="page-title">
            <i class="fas fa-history me-2"></i>My Bookings
          </h2>
          <p class="page-subtitle">
            Manage your parking reservations and view booking history
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="header-actions">
            <button class="btn btn-primary me-2" @click="exportBookings">
              <i class="fas fa-file-download me-1"></i>Export
            </button>
            <router-link to="/user/reserve-parking" class="btn btn-primary">
              <i class="fas fa-plus me-1"></i>New Booking
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <div v-if="activeBooking" class="active-booking-section mb-4">
      <div class="card active-booking-card">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-car me-2"></i>Current Active Booking
          </h6>
        </div>
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-8">
              <div class="active-booking-info">
                <h5 class="booking-location">{{ activeBooking.lot_name }}</h5>
                <div class="booking-details">
                  <div class="detail-item">
                    <i class="fas fa-parking me-1"></i>
                    <span>Spot #{{ activeBooking.spot_number }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="fas fa-car me-1"></i>
                    <span>{{ activeBooking.vehicle_number }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="fas fa-clock me-1"></i>
                    <span>Parked since {{ formatDateTime(activeBooking.parking_timestamp) }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="fas fa-rupee-sign me-1"></i>
                    <span>Current cost: ₹{{ activeBooking.current_cost }}</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-4 text-center">
              <div class="booking-timer">
                <div class="timer-display">
                  <h3>{{ formatDuration(activeBooking.duration) }}</h3>
                  <small>Duration</small>
                </div>
                <div class="booking-actions mt-3">
                  <button class="btn btn-warning me-2" @click="extendBooking(activeBooking)">
                    <i class="fas fa-plus me-1"></i>Extend
                  </button>
                  <button class="btn btn-success" @click="releaseBooking(activeBooking)">
                    <i class="fas fa-sign-out-alt me-1"></i>Release
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="stats-section mb-4">
      <div class="row">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-primary">
              <i class="fas fa-calendar-check"></i>
            </div>
            <div class="stat-content">
              <h4>{{ bookingStats.total }}</h4>
              <p>Total Bookings</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-success">
              <i class="fas fa-check-circle"></i>
            </div>
            <div class="stat-content">
              <h4>{{ bookingStats.completed }}</h4>
              <p>Completed</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-warning">
              <i class="fas fa-clock"></i>
            </div>
            <div class="stat-content">
              <h4>{{ bookingStats.active }}</h4>
              <p>Active</p>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="stat-card">
            <div class="stat-icon bg-info">
              <i class="fas fa-rupee-sign"></i>
            </div>
            <div class="stat-content">
              <h4>₹{{ bookingStats.totalSpent?.toFixed(2) || '0.00' }}</h4>
              <p>Total Spent</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="bookings-history">
      <BookingHistory @release-booking="handleReleaseBooking" />
    </div>
    <div v-if="showExtendModal" class="modal d-block">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-clock me-2"></i>Extend Parking Time
            </h5>
            <button type="button" class="btn-close" @click="closeExtendModal"></button>
          </div>
          <div class="modal-body">
            <div class="extend-booking-form">
              <div class="current-booking-info mb-3">
                <h6 class="text-primary">Current Booking Details</h6>
                <p><strong>Location:</strong> {{ extendingBooking?.lot_name }}</p>
                <p><strong>Spot:</strong> #{{ extendingBooking?.spot_number }}</p>
                <p><strong>Current Duration:</strong> {{ formatDuration(extendingBooking?.duration) }}</p>
                <p><strong>Current Cost:</strong> ₹{{ extendingBooking?.current_cost }}</p>
              </div>
              <div class="extend-options">
                <label class="form-label">Extend by:</label>
                <div class="extend-buttons">
                  <button
                    v-for="option in extendOptions"
                    :key="option.hours"
                    class="btn extend-option"
                    :class="{ active: selectedExtension === option.hours }"
                    @click="selectExtension(option)"
                  >
                    <div class="option-time">{{ option.hours }}h</div>
                    <div class="option-cost">+₹{{ option.cost }}</div>
                  </button>
                </div>
              </div>
              <div v-if="selectedExtension" class="extension-summary mt-3">
                <div class="summary-card">
                  <h6 class="text-primary">Extension Summary</h6>
                  <div class="summary-row">
                    <span>Additional Time:</span>
                    <span>{{ selectedExtension }} hours</span>
                  </div>
                  <div class="summary-row">
                    <span>Additional Cost:</span>
                    <span>₹{{ getExtensionCost(selectedExtension) }}</span>
                  </div>
                  <div class="summary-row total">
                    <span>New Total Duration:</span>
                    <span>{{ getTotalDuration() }} hours</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeExtendModal">
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="!selectedExtension"
              @click="confirmExtension"
            >
              <i class="fas fa-check me-1"></i>Confirm Extension
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showExtendModal" class="modal-backdrop"></div>
    <div v-if="showReleaseModal" class="modal d-block">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-sign-out-alt me-2"></i>Release Parking Spot
            </h5>
            <button type="button" class="btn-close" @click="closeReleaseModal"></button>
          </div>
          <div class="modal-body">
            <div class="release-confirmation">
              <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Are you sure you want to release your parking spot?
              </div>
              <div class="final-summary">
                <h6 class="text-primary">Final Billing Summary</h6>
                <div class="summary-row">
                  <span>Location:</span>
                  <span>{{ releasingBooking?.lot_name }}</span>
                </div>
                <div class="summary-row">
                  <span>Spot Number:</span>
                  <span>#{{ releasingBooking?.spot_number }}</span>
                </div>
                <div class="summary-row">
                  <span>Total Duration:</span>
                  <span>{{ formatDuration(releasingBooking?.duration) }}</span>
                </div>
                <div class="summary-row total">
                  <span>Final Amount:</span>
                  <span class="fw-bold text-primary">₹{{ releasingBooking?.current_cost }}</span>
                </div>
              </div>
              <div class="rating-section mt-3">
                <label class="form-label">Rate your parking experience:</label>
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
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeReleaseModal">
              Cancel
            </button>
            <button type="button" class="btn btn-success" @click="confirmRelease">
              <i class="fas fa-check me-1"></i>Confirm Release
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showReleaseModal" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import BookingHistory from '@/components/user/BookingHistory.vue'
export default {
  name: 'MyBookings',
  components: {
    BookingHistory
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const showExtendModal = ref(false)
    const showReleaseModal = ref(false)
    const extendingBooking = ref(null)
    const releasingBooking = ref(null)
    const selectedExtension = ref(null)
    const releaseRating = ref(5)
    const extendOptions = ref([
      { hours: 1, cost: 50 },
      { hours: 2, cost: 100 },
      { hours: 3, cost: 150 },
      { hours: 4, cost: 200 }
    ])
    const bookingStats = computed(() => userStore.bookingStats)
    const activeBooking = computed(() => userStore.activeBooking)
    const recentBookings = computed(() => userStore.recentBookings)
    const isLoading = computed(() => userStore.isLoading)
    const error = computed(() => userStore.error)
    const formatDateTime = (dateString) => {
      return new Date(dateString).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    const formatDuration = (hours) => {
      if (hours === undefined || hours === null) return '0h 0m';
      const h = Math.floor(hours)
      const m = Math.round((hours - h) * 60)
      return `${h}h ${m}m`
    }
    const extendBooking = (booking) => {
      extendingBooking.value = booking
      selectedExtension.value = null
      showExtendModal.value = true
    }
    const releaseBooking = (booking) => {
      releasingBooking.value = booking;
      releaseRating.value = 5;
      showReleaseModal.value = true;
    };
    const selectExtension = (option) => {
      selectedExtension.value = option.hours
    }
    const getExtensionCost = (hours) => {
      const option = extendOptions.value.find(opt => opt.hours === hours)
      return option ? option.cost : 0
    }
    const getTotalDuration = () => {
      if (!selectedExtension.value || !extendingBooking.value) return 0
      return extendingBooking.value.duration + selectedExtension.value
    }
    const confirmExtension = async () => {
      try {
        await userStore.extendBooking(extendingBooking.value.id, selectedExtension.value)
        closeExtendModal()
      } catch (error) {
        console.error('Error extending booking:', error)
      }
    }
    const confirmRelease = async () => {
      if (!releasingBooking.value) return;
      try {
        await userStore.releaseBooking(releasingBooking.value.id, releaseRating.value);
        closeReleaseModal();
      } catch (error) {
        console.error('Error releasing booking:', error);
      }
    };
    const closeExtendModal = () => {
      showExtendModal.value = false
      extendingBooking.value = null
      selectedExtension.value = null
    }
    const closeReleaseModal = () => {
      showReleaseModal.value = false
      releasingBooking.value = null
      releaseRating.value = 5
    }
    const handleReleaseBooking = (booking) => {
      releaseBooking(booking)
    }
    const exportBookings = async () => {
      try {
        await userStore.exportBookingHistory()
      } catch (error) {
        alert('Error downloading CSV: ' + error.message)
      }
    }
    onMounted(async () => {
      try {
        await userStore.fetchMyBookingsData()
      } catch (error) {
        console.error('Error loading booking data:', error)
      }
    })
    return {
      bookingStats,
      activeBooking,
      recentBookings,
      isLoading,
      error,
      showExtendModal,
      showReleaseModal,
      extendingBooking,
      releasingBooking,
      selectedExtension,
      releaseRating,
      extendOptions,
      formatDateTime,
      formatDuration,
      extendBooking,
      releaseBooking,
      selectExtension,
      getExtensionCost,
      getTotalDuration,
      confirmExtension,
      confirmRelease,
      closeExtendModal,
      closeReleaseModal,
      handleReleaseBooking,
      exportBookings
    }
  }
}
</script>
<style scoped>
.my-bookings {
  padding: 1.5rem;
}
.page-title {
  color: greenyellow;
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
.active-booking-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  border-left: 4px solid var(--secondary-color);
}
.active-booking-card .card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 15px 15px 0 0 !important;
}
.active-booking-card .card-header h6 {
  color: var(--primary-color);
  font-weight: 600;
  margin: 0;
}
.booking-location {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 1rem;
}
.booking-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.detail-item {
  display: flex;
  align-items: center;
  color: #6c757d;
  font-weight: 500;
}
.detail-item i {
  color: var(--secondary-color);
  margin-right: 0.5rem;
}
.timer-display {
  text-align: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.1);
  border-radius: 10px;
  margin-bottom: 1rem;
}
.timer-display h3 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.timer-display small {
  color: #6c757d;
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
.stat-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.stat-content h4 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.stat-content p {
  color: #6c757d;
  margin: 0;
}
.extend-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.extend-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.1);
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 10px;
  transition: all 0.3s ease;
}
.extend-option:hover {
  background: rgba(138, 184, 254, 0.2);
  border-color: var(--secondary-color);
}
.extend-option.active {
  background: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
.option-time {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.option-cost {
  font-size: 0.9rem;
  opacity: 0.8;
}
.summary-card {
  background: rgba(138, 184, 254, 0.1);
  border-radius: 10px;
  padding: 1rem;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.summary-row:last-child {
  margin-bottom: 0;
}
.summary-row.total {
  border-top: 2px solid rgba(138, 184, 254, 0.3);
  padding-top: 0.5rem;
  margin-top: 0.5rem;
  font-weight: 600;
}
.final-summary {
  background: rgba(138, 184, 254, 0.1);
  border-radius: 10px;
  padding: 1rem;
  margin-top: 1rem;
}
.star-rating {
  display: flex;
  gap: 0.25rem;
  margin-top: 0.5rem;
}
.star-btn {
  background: none;
  border: none;
  color: #ddd;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.star-btn:hover,
.star-btn.active {
  color: #ffc107;
  transform: scale(1.1);
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
</style>