<template>
  <div class="reserve-parking">
    
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h2 class="page-title">
            <i class="fas fa-parking me-2"></i>Reserve Parking
          </h2>
          <p class="page-subtitle">
            Find and book the perfect parking spot for your needs
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="header-actions">
            <button class="btn btn-outline-primary me-2" @click="showFilters = !showFilters">
              <i class="fas fa-filter me-1"></i>Filters
            </button>
            <button class="btn btn-primary" @click="refreshLocations">
              <i class="fas fa-sync me-1"></i>Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="search-section mb-4">
      <div class="card">
        <div class="card-body">
          <div class="row">
            <div class="col-md-4">
              <label class="form-label">Location</label>
              <div class="location-input">
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fas fa-map-marker-alt"></i>
                  </span>
                  <input
                    v-model="searchCriteria.location"
                    type="text"
                    class="form-control"
                    placeholder="Enter location or area..."
                    @keyup.enter="searchParkingLots"
                  >
                </div>
              </div>
            </div>
            <div class="col-md-2">
              <label class="form-label">Date</label>
              <input
                v-model="searchCriteria.date"
                type="date"
                class="form-control"
                :min="today"
              >
            </div>
            <div class="col-md-2">
              <label class="form-label">Time</label>
              <input
                v-model="searchCriteria.time"
                type="time"
                class="form-control"
              >
            </div>
            <div class="col-md-2">
              <label class="form-label">Duration</label>
              <select v-model="searchCriteria.duration" class="form-select">
                <option value="1">1 hour</option>
                <option value="2">2 hours</option>
                <option value="3">3 hours</option>
                <option value="4">4 hours</option>
                <option value="6">6 hours</option>
                <option value="8">8 hours</option>
                <option value="12">12 hours</option>
                <option value="24">24 hours</option>
              </select>
            </div>
            <div class="col-md-2 d-flex align-items-end">
              <button class="btn btn-primary w-100" @click="searchParkingLots">
                <i class="fas fa-search me-1"></i>Search
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showFilters" class="filters-panel mb-4">
      <div class="card">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-filter me-2"></i>Advanced Filters
          </h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-3">
              <label class="form-label">Price Range</label>
              <div class="price-range">
                <div class="input-group">
                  <span class="input-group-text">₹</span>
                  <input v-model="filters.priceMin" type="number" class="form-control" placeholder="Min">
                  <span class="input-group-text">to</span>
                  <input v-model="filters.priceMax" type="number" class="form-control" placeholder="Max">
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <label class="form-label">Distance</label>
              <select v-model="filters.distance" class="form-select">
                <option value="">Any distance</option>
                <option value="1">Within 1 km</option>
                <option value="2">Within 2 km</option>
                <option value="5">Within 5 km</option>
                <option value="10">Within 10 km</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label">Features</label>
              <div class="features-checkboxes">
                <div class="form-check">
                  <input v-model="filters.features.security" class="form-check-input" type="checkbox" id="security">
                  <label class="form-check-label" for="security">24/7 Security</label>
                </div>
                <div class="form-check">
                  <input v-model="filters.features.covered" class="form-check-input" type="checkbox" id="covered">
                  <label class="form-check-label" for="covered">Covered Parking</label>
                </div>
              </div>
            </div>
            <div class="col-md-3 d-flex align-items-end">
              <button class="btn btn-outline-secondary me-2" @click="clearFilters">
                <i class="fas fa-times me-1"></i>Clear
              </button>
              <button class="btn btn-primary" @click="applyFilters">
                <i class="fas fa-check me-1"></i>Apply
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="steps-indicator mb-4">
      <div class="steps-container">
        <div class="step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
          <div class="step-circle">
            <i class="fas" :class="currentStep > 1 ? 'fa-check' : 'fa-search'"></i>
          </div>
          <span>Find Location</span>
        </div>
        <div class="step-line"></div>
        <div class="step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
          <div class="step-circle">
            <i class="fas" :class="currentStep > 2 ? 'fa-check' : 'fa-car'"></i>
          </div>
          <span>Book Spot</span>
        </div>
        <div class="step-line"></div>
        <div class="step" :class="{ active: currentStep >= 3 }">
          <div class="step-circle">
            <i class="fas fa-check-circle"></i>
          </div>
          <span>Confirmation</span>
        </div>
      </div>
    </div>
    
    <div v-if="currentStep === 1" class="parking-selection-step">
      
      <ParkingSelection @lot-selected="handleLotSelected" />
    </div>
    <div v-else-if="currentStep === 2" class="booking-step">
      
      <SpotBooking
        :selected-lot="selectedLot"
        @booking-success="handleBookingSuccess"
        @back-to-selection="currentStep = 1"
      />
    </div>
    <div v-else-if="currentStep === 3" class="confirmation-step">
      
      <div class="confirmation-card">
        <div class="card">
          <div class="card-header bg-success text-white text-center">
            <h5 class="mb-0">
              <i class="fas fa-check-circle me-2"></i>
              Booking Confirmed!
            </h5>
          </div>
          <div class="card-body text-center">
            <div class="confirmation-animation mb-4">
              <i class="fas fa-car confirmation-icon"></i>
              <div class="success-checkmark">
                <i class="fas fa-check"></i>
              </div>
            </div>
            <h4 class="confirmation-title">Your parking spot is reserved!</h4>
            <p class="confirmation-message">
              We've sent a confirmation email with all the details to your registered email address.
            </p>
            <div class="booking-summary">
              <div class="summary-card">
                <h6 class="text-primary mb-3">Booking Summary</h6>
                <div class="summary-row">
                  <span>Booking ID:</span>
                  <span class="fw-bold">#{{ bookingDetails.id }}</span>
                </div>
                <div class="summary-row">
                  <span>Location:</span>
                  <span>{{ bookingDetails.location }}</span>
                </div>
                <div class="summary-row">
                  <span>Spot Number:</span>
                  <span class="fw-bold">#{{ bookingDetails.spotNumber }}</span>
                </div>
                <div class="summary-row">
                  <span>Date & Time:</span>
                  <span>{{ bookingDetails.dateTime }}</span>
                </div>
                <div class="summary-row">
                  <span>Duration:</span>
                  <span>{{ bookingDetails.duration }} hours</span>
                </div>
                <div class="summary-row total">
                  <span>Total Cost:</span>
                  <span class="fw-bold text-primary">₹{{ bookingDetails.cost }}</span>
                </div>
              </div>
            </div>
            <div class="confirmation-actions">
              <button class="btn btn-outline-primary me-2" @click="downloadReceipt">
                <i class="fas fa-download me-1"></i>Download Receipt
              </button>
              <router-link to="/user/my-bookings" class="btn btn-primary me-2">
                <i class="fas fa-history me-1"></i>View My Bookings
              </router-link>
              <button class="btn btn-success" @click="startNewBooking">
                <i class="fas fa-plus me-1"></i>Book Another
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="quick-tips-sidebar" :class="{ 'show': showTips }">
      <div class="tips-content">
        <div class="tips-header">
          <h6>
            <i class="fas fa-lightbulb me-2"></i>Parking Tips
          </h6>
          <button class="btn-close" @click="showTips = false"></button>
        </div>
        <div class="tips-list">
          <div class="tip-item">
            <i class="fas fa-clock text-primary"></i>
            <div>
              <strong>Book in Advance</strong>
              <p>Reserve 30 minutes before arrival for guaranteed spots</p>
            </div>
          </div>
          <div class="tip-item">
            <i class="fas fa-money-bill-wave text-success"></i>
            <div>
              <strong>Save Money</strong>
              <p>Off-peak hours (10 AM - 4 PM) have lower rates</p>
            </div>
          </div>
          <div class="tip-item">
            <i class="fas fa-mobile-alt text-info"></i>
            <div>
              <strong>Mobile Notifications</strong>
              <p>Enable notifications for booking reminders</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <button class="tips-toggle-btn" @click="showTips = !showTips">
      <i class="fas fa-question-circle"></i>
    </button>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useParkingStore } from '../../store/modules/parking'
import ParkingSelection from '../../components/user/ParkingSelection.vue'
import SpotBooking from '../../components/user/SpotBooking.vue'
export default {
  name: 'ReserveParking',
  components: {
    ParkingSelection,
    SpotBooking
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const parkingStore = useParkingStore()
    const currentStep = ref(1)
    const showFilters = ref(false)
    const showTips = ref(false)
    const selectedLot = ref(null)
    const searchCriteria = reactive({
      location: '',
      date: '',
      time: '',
      duration: '2'
    })
    const filters = reactive({
      priceMin: '',
      priceMax: '',
      distance: '',
      features: {
        security: false,
        covered: false
      }
    })
    const bookingDetails = ref({
      id: '',
      location: '',
      spotNumber: '',
      dateTime: '',
      duration: '',
      cost: ''
    })
    const today = computed(() => new Date().toISOString().split('T')[0])
    const searchParkingLots = () => {
      console.log('Searching parking lots with criteria:', searchCriteria)
    }
    const handleLotSelected = (lot) => {
      selectedLot.value = lot
      currentStep.value = 2
    }
    const handleBookingSuccess = (details) => {
      bookingDetails.value = details
      currentStep.value = 3
    }
    const clearFilters = () => {
      filters.priceMin = ''
      filters.priceMax = ''
      filters.distance = ''
      filters.features.security = false
      filters.features.covered = false
    }
    const applyFilters = () => {
      console.log('Applying filters:', filters)
      showFilters.value = false
      searchParkingLots()
    }
    const refreshLocations = () => {
      parkingStore.fetchAvailableLots(true)
    }
    const downloadReceipt = () => {
      console.log('Downloading receipt for booking:', bookingDetails.value.id)
    }
    const startNewBooking = () => {
      currentStep.value = 1
      selectedLot.value = null
      bookingDetails.value = {}
    }
    onMounted(() => {
      searchCriteria.date = today.value
      searchCriteria.time = new Date().toTimeString().slice(0, 5)
      if (route.query.location) {
        searchCriteria.location = route.query.location
      }
      if (route.query.date) {
        searchCriteria.date = route.query.date
      }
      if (route.query.time) {
        searchCriteria.time = route.query.time
      }
      if (route.query.location || route.query.date) {
        searchParkingLots()
      }
    })
    return {
      currentStep,
      showFilters,
      showTips,
      selectedLot,
      searchCriteria,
      filters,
      bookingDetails,
      today,
      searchParkingLots,
      handleLotSelected,
      handleBookingSuccess,
      clearFilters,
      applyFilters,
      refreshLocations,
      downloadReceipt,
      startNewBooking
    }
  }
}
</script>
<style scoped>
.reserve-parking {
  padding: 1.5rem;
  position: relative;
}
.page-title {
  color: yellow;
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
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 15px 15px 0 0 !important;
  padding: 1.25rem;
}
.card-header h6 {
  color: var(--primary-color);
  font-weight: 600;
  margin: 0;
}
.input-group-text {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: rgba(138, 184, 254, 0.3);
  color: var(--secondary-color);
}
.form-control, .form-select {
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 8px;
  transition: all 0.3s ease;
}
.form-control:focus, .form-select:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
}
.steps-indicator {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.steps-container {
  display: flex;
  align-items: center;
  justify-content: center;
  max-width: 600px;
  margin: 0 auto;
}
.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  opacity: 0.5;
  transition: all 0.3s ease;
}
.step.active {
  opacity: 1;
}
.step.completed {
  opacity: 1;
}
.step-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: #dee2e6;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  transition: all 0.3s ease;
}
.step.active .step-circle {
  background: var(--secondary-color);
  color: white;
}
.step.completed .step-circle {
  background: #28a745;
  color: white;
}
.step span {
  font-size: 0.9rem;
  font-weight: 600;
  color: #6c757d;
  text-align: center;
}
.step.active span,
.step.completed span {
  color: var(--primary-color);
}
.step-line {
  width: 100px;
  height: 2px;
  background: #dee2e6;
  margin: 0 1rem;
}
.confirmation-animation {
  position: relative;
  display: inline-block;
}
.confirmation-icon {
  font-size: 4rem;
  color: var(--secondary-color);
  animation: bounce 1s ease-in-out;
}
.success-checkmark {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 30px;
  height: 30px;
  background: #28a745;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  animation: pop 0.6s ease-out 0.5s both;
}
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}
@keyframes pop {
  0% { transform: scale(0); }
  80% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
.confirmation-title {
  color: var(--primary-color);
  margin-bottom: 1rem;
}
.confirmation-message {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}
.summary-card {
  background: rgba(138, 184, 254, 0.1);
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.summary-row:last-child {
  margin-bottom: 0;
}
.summary-row.total {
  border-top: 2px solid rgba(138, 184, 254, 0.3);
  padding-top: 0.75rem;
  margin-top: 1rem;
  font-size: 1.1rem;
}
.quick-tips-sidebar {
  position: fixed;
  top: 50%;
  right: -350px;
  transform: translateY(-50%);
  width: 320px;
  background: white;
  border-radius: 15px 0 0 15px;
  box-shadow: -5px 0 15px rgba(0, 1, 51, 0.1);
  transition: all 0.3s ease;
  z-index: 1000;
}
.quick-tips-sidebar.show {
  right: 0;
}
.tips-content {
  padding: 1.5rem;
}
.tips-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  color: var(--primary-color);
}
.tips-header h6 {
  margin: 0;
  font-weight: 600;
}
.tip-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
}
.tip-item i {
  font-size: 1.25rem;
  margin-right: 1rem;
  margin-top: 0.25rem;
}
.tip-item strong {
  color: var(--primary-color);
  display: block;
  margin-bottom: 0.25rem;
}
.tip-item p {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}
.tips-toggle-btn {
  position: fixed;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  background: var(--secondary-color);
  color: white;
  border: none;
  border-radius: 50%;
  font-size: 1.25rem;
  box-shadow: 0 5px 15px rgba(75, 0, 110, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 999;
}
.tips-toggle-btn:hover {
  background: var(--primary-color);
  transform: translateY(-50%) scale(1.1);
}
.form-check-input:checked {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
@media (max-width: 768px) {
  .reserve-parking {
    padding: 1rem;
  }
  .header-actions {
    margin-top: 1rem;
  }
  .steps-container {
    flex-direction: column;
    gap: 1rem;
  }
  .step-line {
    width: 2px;
    height: 30px;
    margin: 0.5rem 0;
  }
  .quick-tips-sidebar {
    position: fixed;
    top: auto;
    bottom: -300px;
    right: 0;
    left: 0;
    width: auto;
    border-radius: 15px 15px 0 0;
    transform: none;
  }
  .quick-tips-sidebar.show {
    bottom: 0;
  }
  .tips-toggle-btn {
    bottom: 20px;
    top: auto;
    transform: none;
  }
}
</style>