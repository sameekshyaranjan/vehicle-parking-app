<template>
  <div class="spot-release">
    
    <div class="release-header mb-4">
      <h4 class="text-primary mb-1">
        <i class="fas fa-sign-out-alt me-2"></i>Release Parking Spot
      </h4>
      <p class="text-muted mb-0">Complete your parking session and checkout</p>
    </div>
    
    <div v-if="activeReservation" class="card booking-info-card mb-4">
      <div class="card-header">
        <h6 class="mb-0">
          <i class="fas fa-info-circle me-2"></i>
          Current Parking Session
        </h6>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-8">
            <div class="booking-details">
              <h5 class="location-name">{{ activeReservation.lot_name }}</h5>
              <p class="booking-info">
                <i class="fas fa-map-marker-alt me-1"></i>
                {{ activeReservation.lot_address }}
              </p>
              <div class="session-details">
                <div class="detail-row">
                  <span class="detail-label">
                    <i class="fas fa-car me-1"></i>Vehicle:
                  </span>
                  <span class="detail-value">{{ activeReservation.vehicle_number }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">
                    <i class="fas fa-parking me-1"></i>Spot:
                  </span>
                  <span class="detail-value">#{{ activeReservation.spot_number }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">
                    <i class="fas fa-clock me-1"></i>Check-in:
                  </span>
                  <span class="detail-value">{{ formatDateTime(activeReservation.parking_timestamp) }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">
                    <i class="fas fa-hourglass-half me-1"></i>Duration:
                  </span>
                  <span class="detail-value duration-highlight">{{ currentDuration }}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4 text-center">
            <div class="session-timer">
              <div class="timer-circle">
                <h3 class="timer-hours">{{ timerHours }}</h3>
                <small>hours</small>
              </div>
              <div class="timer-cost">
                <h4 class="current-cost">₹{{ currentCost }}</h4>
                <small class="text-muted">Current Cost</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card release-form-card">
      <div class="card-header">
        <h6 class="mb-0">
          <i class="fas fa-edit me-2"></i>
          Checkout Details
        </h6>
      </div>
      <div class="card-body">
        
        <div v-if="error" class="alert alert-danger" role="alert">
          <i class="fas fa-exclamation-triangle me-2"></i>
          {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success" role="alert">
          <i class="fas fa-check-circle me-2"></i>
          {{ successMessage }}
        </div>
        
        <form @submit.prevent="handleRelease">
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="releaseTime" class="form-label">
                <i class="fas fa-calendar-times me-1"></i>
                Release Date & Time <span class="text-danger">*</span>
              </label>
              <input
                id="releaseTime"
                v-model="form.leaving_timestamp"
                type="datetime-local"
                class="form-control"
                :class="{ 'is-invalid': errors.leaving_timestamp }"
                :min="minReleaseTime"
                :max="maxReleaseTime"
                required
                :disabled="isLoading"
                @change="calculateFinalCost"
              >
              <div v-if="errors.leaving_timestamp" class="invalid-feedback">
                {{ errors.leaving_timestamp }}
              </div>
              <div class="form-text">Default is current time</div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="vehicleCondition" class="form-label">
                <i class="fas fa-car-crash me-1"></i>
                Vehicle Condition
              </label>
              <select
                id="vehicleCondition"
                v-model="form.vehicle_condition"
                class="form-select"
                :disabled="isLoading"
              >
                <option value="good">Good - No Issues</option>
                <option value="minor_damage">Minor Damage</option>
                <option value="major_damage">Major Damage</option>
              </select>
            </div>
          </div>
          
          <div class="mb-3">
            <label class="form-label">
              <i class="fas fa-star me-1"></i>
              Rate Your Experience
            </label>
            <div class="rating-section">
              <div class="star-rating">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  class="star-btn"
                  :class="{ active: star <= form.rating }"
                  @click="form.rating = star"
                  :disabled="isLoading"
                >
                  <i class="fas fa-star"></i>
                </button>
              </div>
              <span class="rating-text">{{ getRatingText(form.rating) }}</span>
            </div>
          </div>
          
          <div class="mb-4">
            <label for="feedback" class="form-label">
              <i class="fas fa-comment me-1"></i>
              Feedback & Comments (Optional)
            </label>
            <textarea
              id="feedback"
              v-model="form.feedback"
              class="form-control"
              rows="3"
              placeholder="Share your experience, report any issues..."
              :disabled="isLoading"
            ></textarea>
          </div>
          
          <div class="cost-breakdown mb-4">
            <div class="breakdown-header">
              <h6 class="text-primary">
                <i class="fas fa-receipt me-2"></i>Final Bill
              </h6>
            </div>
            <div class="breakdown-body">
              <div class="breakdown-row">
                <span>Base Rate (₹{{ hourlyRate }}/hour)</span>
                <span>₹{{ hourlyRate }}</span>
              </div>
              <div class="breakdown-row">
                <span>Total Duration</span>
                <span>{{ finalDuration }} hours</span>
              </div>
              <div class="breakdown-row">
                <span>Subtotal</span>
                <span>₹{{ subtotal }}</span>
              </div>
              <div v-if="overtimeCharges > 0" class="breakdown-row warning">
                <span>Overtime Charges (25% extra)</span>
                <span>+₹{{ overtimeCharges }}</span>
              </div>
              <div v-if="earlyBirdDiscount > 0" class="breakdown-row success">
                <span>Early Bird Discount</span>
                <span>-₹{{ earlyBirdDiscount }}</span>
              </div>
              <div v-if="damageCharges > 0" class="breakdown-row danger">
                <span>Damage Charges</span>
                <span>+₹{{ damageCharges }}</span>
              </div>
              <hr>
              <div class="breakdown-row total">
                <span class="fw-bold">Final Amount</span>
                <span class="fw-bold text-primary">₹{{ finalCost }}</span>
              </div>
            </div>
          </div>
          
          <div class="payment-section mb-4">
            <h6 class="text-primary mb-3">
              <i class="fas fa-credit-card me-2"></i>Payment Method
            </h6>
            <div class="payment-options">
              <div class="form-check payment-option">
                <input
                  id="paymentCash"
                  v-model="form.payment_method"
                  type="radio"
                  class="form-check-input"
                  value="cash"
                  :disabled="isLoading"
                >
                <label for="paymentCash" class="form-check-label">
                  <i class="fas fa-money-bill-wave me-2"></i>
                  Cash Payment
                </label>
              </div>
              <div class="form-check payment-option">
                <input
                  id="paymentCard"
                  v-model="form.payment_method"
                  type="radio"
                  class="form-check-input"
                  value="card"
                  :disabled="isLoading"
                >
                <label for="paymentCard" class="form-check-label">
                  <i class="fas fa-credit-card me-2"></i>
                  Card Payment
                </label>
              </div>
              <div class="form-check payment-option">
                <input
                  id="paymentUPI"
                  v-model="form.payment_method"
                  type="radio"
                  class="form-check-input"
                  value="upi"
                  :disabled="isLoading"
                >
                <label for="paymentUPI" class="form-check-label">
                  <i class="fas fa-mobile-alt me-2"></i>
                  UPI Payment
                </label>
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-between align-items-center">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="$emit('cancel')"
              :disabled="isLoading"
            >
              <i class="fas fa-times me-1"></i>Cancel
            </button>
            <div class="d-flex gap-2">
              <button
                type="button"
                class="btn btn-warning"
                @click="extendBooking"
                :disabled="isLoading"
              >
                <i class="fas fa-clock me-1"></i>Extend Time
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isLoading || !form.payment_method"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-sign-out-alt me-1"></i>
                {{ isLoading ? 'Processing...' : 'Complete Checkout' }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
    
    <div v-if="showConfirmation" class="modal d-block">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-success text-white">
            <h5 class="modal-title">
              <i class="fas fa-check-circle me-2"></i>
              Checkout Complete!
            </h5>
          </div>
          <div class="modal-body text-center">
            <div class="success-icon mb-3">
              <i class="fas fa-thumbs-up text-success"></i>
            </div>
            <h5>Thank you for using our parking service!</h5>
            <p class="text-muted">Your parking session has been completed successfully.</p>
            <div class="receipt-summary">
              <h6 class="text-primary">Receipt Summary</h6>
              <div class="summary-row">
                <span>Session Duration:</span>
                <span>{{ finalDuration }} hours</span>
              </div>
              <div class="summary-row">
                <span>Total Amount:</span>
                <span class="fw-bold">₹{{ finalCost }}</span>
              </div>
              <div class="summary-row">
                <span>Payment Method:</span>
                <span>{{ getPaymentMethodText(form.payment_method) }}</span>
              </div>
              <div class="summary-row">
                <span>Receipt ID:</span>
                <span>#{{ receiptId }}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="goToDashboard">
              <i class="fas fa-home me-1"></i>Go to Dashboard
            </button>
            <button type="button" class="btn btn-outline-primary" @click="downloadReceipt">
              <i class="fas fa-download me-1"></i>Download Receipt
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showConfirmation" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '../../store/modules/parking'
export default {
  name: 'SpotRelease',
  props: {
    reservation: {
      type: Object,
      default: null
    }
  },
  emits: ['cancel', 'released'],
  setup(props, { emit }) {
    const router = useRouter()
    const parkingStore = useParkingStore()
    const isLoading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const showConfirmation = ref(false)
    const receiptId = ref('')
    const currentTime = ref(new Date())
    const timer = ref(null)
    const form = reactive({
      leaving_timestamp: '',
      vehicle_condition: 'good',
      rating: 5,
      feedback: '',
      payment_method: 'cash'
    })
    const errors = reactive({
      leaving_timestamp: ''
    })
    const activeReservation = computed(() =>
      props.reservation || parkingStore.activeReservation
    )
    const minReleaseTime = computed(() => {
      if (!activeReservation.value) return ''
      return new Date(activeReservation.value.parking_timestamp).toISOString().slice(0, 16)
    })
    const maxReleaseTime = computed(() => {
      return new Date().toISOString().slice(0, 16)
    })
    const currentDuration = computed(() => {
      if (!activeReservation.value) return '0h 0m'
      const start = new Date(activeReservation.value.parking_timestamp)
      const end = currentTime.value
      const diffMs = end - start
      const hours = Math.floor(diffMs / (1000 * 60 * 60))
      const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      return `${hours}h ${minutes}m`
    })
    const timerHours = computed(() => {
      if (!activeReservation.value) return '0'
      const start = new Date(activeReservation.value.parking_timestamp)
      const end = currentTime.value
      const diffMs = end - start
      const hours = Math.floor(diffMs / (1000 * 60 * 60))
      return hours.toString()
    })
    const finalDuration = computed(() => {
      if (!activeReservation.value || !form.leaving_timestamp) return 0
      const start = new Date(activeReservation.value.parking_timestamp)
      const end = new Date(form.leaving_timestamp)
      const diffMs = end - start
      const hours = Math.ceil(diffMs / (1000 * 60 * 60))
      return Math.max(1, hours)
    })
    const hourlyRate = computed(() => activeReservation.value?.hourly_rate || 50)
    const subtotal = computed(() => finalDuration.value * hourlyRate.value)
    const overtimeCharges = computed(() => {
      const expectedDuration = activeReservation.value?.expected_duration || 2
      if (finalDuration.value > expectedDuration) {
        const overtimeHours = finalDuration.value - expectedDuration
        return Math.round(overtimeHours * hourlyRate.value * 0.25)
      }
      return 0
    })
    const earlyBirdDiscount = computed(() => {
      if (activeReservation.value?.booked_in_advance) {
        return Math.round(subtotal.value * 0.1)
      }
      return 0
    })
    const damageCharges = computed(() => {
      switch (form.vehicle_condition) {
        case 'minor_damage':
          return 500
        case 'major_damage':
          return 2000
        default:
          return 0
      }
    })
    const finalCost = computed(() => {
      return Math.max(0, subtotal.value + overtimeCharges.value + damageCharges.value - earlyBirdDiscount.value)
    })
    const currentCost = computed(() => {
      if (!activeReservation.value) return 0
      const start = new Date(activeReservation.value.parking_timestamp)
      const end = currentTime.value
      const diffMs = end - start
      const hours = Math.ceil(diffMs / (1000 * 60 * 60))
      return Math.max(hours * hourlyRate.value, hourlyRate.value)
    })
    const calculateFinalCost = () => {
    }
    const getRatingText = (rating) => {
      const texts = {
        1: 'Poor',
        2: 'Fair',
        3: 'Good',
        4: 'Very Good',
        5: 'Excellent'
      }
      return texts[rating] || 'Not Rated'
    }
    const getPaymentMethodText = (method) => {
      const texts = {
        cash: 'Cash Payment',
        card: 'Card Payment',
        upi: 'UPI Payment'
      }
      return texts[method] || method
    }
    const validateForm = () => {
      errors.leaving_timestamp = ''
      if (!form.leaving_timestamp) {
        errors.leaving_timestamp = 'Release time is required'
        return false
      }
      const releaseTime = new Date(form.leaving_timestamp)
      const startTime = new Date(activeReservation.value.parking_timestamp)
      if (releaseTime <= startTime) {
        errors.leaving_timestamp = 'Release time must be after check-in time'
        return false
      }
      if (releaseTime > currentTime.value) {
        errors.leaving_timestamp = 'Release time cannot be in the future'
        return false
      }
      return true
    }
    const handleRelease = async () => {
      if (!validateForm()) return
      isLoading.value = true
      error.value = ''
      successMessage.value = ''
      try {
        const releaseData = {
          reservation_id: activeReservation.value.id,
          leaving_timestamp: form.leaving_timestamp,
          final_cost: finalCost.value,
          duration_hours: finalDuration.value,
          rating: form.rating,
          feedback: form.feedback,
          payment_method: form.payment_method,
          vehicle_condition: form.vehicle_condition
        }
        const result = await parkingStore.releaseParkingSpot(activeReservation.value.id, releaseData)
        if (result.success) {
          receiptId.value = result.receipt_id
          showConfirmation.value = true
          successMessage.value = 'Parking spot released successfully!'
          emit('released', result)
        }
      } catch (err) {
        error.value = err.message || 'Release failed. Please try again.'
      } finally {
        isLoading.value = false
      }
    }
    const extendBooking = () => {
      router.push({
        path: '/user/extend-booking',
        query: { reservationId: activeReservation.value?.id }
      })
    }
    const goToDashboard = () => {
      showConfirmation.value = false
      router.push('/user/dashboard')
    }
    const downloadReceipt = () => {
      console.log('Downloading receipt:', receiptId.value)
      showConfirmation.value = false
    }
    const formatDateTime = (dateString) => {
      return new Date(dateString).toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    const startTimer = () => {
      timer.value = setInterval(() => {
        currentTime.value = new Date()
      }, 60000)
    }
    const stopTimer = () => {
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
    }
    onMounted(() => {
      form.leaving_timestamp = new Date().toISOString().slice(0, 16)
      startTimer()
      if (!props.reservation) {
        parkingStore.fetchActiveReservation()
      }
    })
    onUnmounted(() => {
      stopTimer()
    })
    return {
      isLoading,
      error,
      successMessage,
      showConfirmation,
      receiptId,
      form,
      errors,
      activeReservation,
      minReleaseTime,
      maxReleaseTime,
      currentDuration,
      timerHours,
      finalDuration,
      hourlyRate,
      subtotal,
      overtimeCharges,
      earlyBirdDiscount,
      damageCharges,
      finalCost,
      currentCost,
      calculateFinalCost,
      getRatingText,
      getPaymentMethodText,
      handleRelease,
      extendBooking,
      goToDashboard,
      downloadReceipt,
      formatDateTime
    }
  }
}
</script>
<style scoped>
.spot-release {
  padding: 1rem;
}
.text-primary {
  color: var(--primary-color) !important;
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.btn-warning {
  background-color: #fd7e14;
  border-color: #fd7e14;
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-secondary {
  border-radius: 8px;
  font-weight: 600;
}
.booking-info-card, .release-form-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.booking-info-card .card-header,
.release-form-card .card-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  border-radius: 15px 15px 0 0 !important;
}
.location-name {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.booking-info {
  color: #6c757d;
  margin-bottom: 1rem;
}
.session-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.detail-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.detail-label {
  color: #6c757d;
  min-width: 100px;
}
.detail-value {
  color: var(--primary-color);
  font-weight: 600;
}
.duration-highlight {
  color: var(--secondary-color) !important;
  font-size: 1.1rem;
}
.session-timer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.timer-circle {
  width: 100px;
  height: 100px;
  border: 4px solid var(--text-accent);
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
}
.timer-hours {
  color: var(--primary-color);
  font-weight: 700;
  margin: 0;
  font-size: 2rem;
}
.timer-cost {
  text-align: center;
}
.current-cost {
  color: var(--secondary-color);
  font-weight: 700;
  margin: 0;
}
.form-label {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.form-control, .form-select {
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}
.form-control:focus, .form-select:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
}
.rating-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.star-rating {
  display: flex;
  gap: 0.25rem;
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
.rating-text {
  color: var(--secondary-color);
  font-weight: 600;
}
.cost-breakdown {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid rgba(138, 184, 254, 0.2);
}
.breakdown-header h6 {
  margin-bottom: 1rem;
}
.breakdown-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.breakdown-row.warning {
  color: #fd7e14;
  font-weight: 600;
}
.breakdown-row.success {
  color: #28a745;
  font-weight: 600;
}
.breakdown-row.danger {
  color: #dc3545;
  font-weight: 600;
}
.breakdown-row.total {
  font-size: 1.1rem;
  color: var(--primary-color);
}
.payment-section {
  background: rgba(138, 184, 254, 0.05);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid rgba(138, 184, 254, 0.2);
}
.payment-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.payment-option {
  background: white;
  padding: 1rem;
  border-radius: 8px;
  border: 2px solid rgba(138, 184, 254, 0.2);
  transition: all 0.3s ease;
}
.payment-option:hover {
  border-color: var(--secondary-color);
}
.payment-option .form-check-input:checked + .form-check-label {
  color: var(--primary-color);
  font-weight: 600;
}
.form-check-input:checked {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.alert {
  border: none;
  border-radius: 10px;
}
.alert-success {
  background: linear-gradient(135deg, rgba(40, 167, 69, 0.1), rgba(255, 255, 255, 0.9));
  border-left: 4px solid #28a745;
}
.alert-danger {
  background: linear-gradient(135deg, rgba(220, 53, 69, 0.1), rgba(255, 255, 255, 0.9));
  border-left: 4px solid #dc3545;
}
.success-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}
.receipt-summary {
  background: rgba(138, 184, 254, 0.1);
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
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
.gap-2 {
  gap: 0.5rem;
}
@media (max-width: 768px) {
  .session-details {
    margin-bottom: 1rem;
  }
  .timer-circle {
    width: 80px;
    height: 80px;
  }
  .timer-hours {
    font-size: 1.5rem;
  }
  .payment-options {
    gap: 0.5rem;
  }
  .d-flex.justify-content-between {
    flex-direction: column;
    gap: 1rem;
  }
  .d-flex.gap-2 {
    width: 100%;
  }
  .d-flex.gap-2 .btn {
    flex: 1;
  }
}
</style>