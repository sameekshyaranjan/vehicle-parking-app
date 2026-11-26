<template>
  <div class="spot-booking">
    
    <div class="booking-header mb-4">
      <h4 class="text-primary mb-1">
        <i class="fas fa-parking me-2"></i>Book Your Parking Spot
      </h4>
      <p class="text-muted mb-0">Reserve your parking space in {{ selectedLot?.prime_location_name || 'selected location' }}</p>
    </div>
    
    <div v-if="selectedLot" class="card location-card mb-4">
      <div class="card-header">
        <h6 class="mb-0">
          <i class="fas fa-map-marker-alt me-2"></i>
          Selected Location
        </h6>
      </div>
      <div class="card-body">
        <div class="row">
          <div class="col-md-8">
            <h5 class="location-name">{{ selectedLot.prime_location_name }}</h5>
            <p class="location-address">
              <i class="fas fa-home me-1"></i>
              {{ selectedLot.address }}
            </p>
            <div class="location-meta">
              <span class="meta-item">
                <i class="fas fa-rupee-sign me-1"></i>
                ₹{{ selectedLot.price }}/hour
              </span>
              <span class="meta-item">
                <i class="fas fa-car me-1"></i>
                {{ selectedLot.available_spots }} spots available
              </span>
              <span class="meta-item">
                <i class="fas fa-map-pin me-1"></i>
                {{ selectedLot.pin_code }}
              </span>
            </div>
          </div>
          <div class="col-md-4 text-center">
            <div class="availability-circle">
              <div class="circle-content">
                <h3>{{ selectedLot.available_spots }}</h3>
                <small>Available</small>
              </div>
            </div>
            <button class="btn btn-outline-primary btn-sm mt-2" @click="changeLocation">
              <i class="fas fa-exchange-alt me-1"></i>Change Location
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card booking-form-card">
      <div class="card-header">
        <h6 class="mb-0">
          <i class="fas fa-edit me-2"></i>
          Booking Details
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
        
        <form @submit.prevent="handleBooking">
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="vehicleNumber" class="form-label">
                <i class="fas fa-car me-1"></i>
                Vehicle Number <span class="text-danger">*</span>
              </label>
              <input
                id="vehicleNumber"
                v-model="form.vehicle_number"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.vehicle_number }"
                placeholder="e.g., KA-01-AB-1234"
                required
                :disabled="isLoading"
                @input="validateVehicleNumber"
              >
              <div v-if="errors.vehicle_number" class="invalid-feedback">
                {{ errors.vehicle_number }}
              </div>
              <div class="form-text">Enter your vehicle registration number</div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="duration" class="form-label">
                <i class="fas fa-clock me-1"></i>
                Expected Duration <span class="text-danger">*</span>
              </label>
              <select
                id="duration"
                v-model="form.expected_duration"
                class="form-select"
                :class="{ 'is-invalid': errors.expected_duration }"
                required
                :disabled="isLoading"
                @change="calculateEstimatedCost"
              >
                <option value="">Select duration</option>
                <option value="1">1 hour</option>
                <option value="2">2 hours</option>
                <option value="3">3 hours</option>
                <option value="4">4 hours</option>
                <option value="6">6 hours</option>
                <option value="8">8 hours</option>
                <option value="12">12 hours</option>
                <option value="24">24 hours</option>
              </select>
              <div v-if="errors.expected_duration" class="invalid-feedback">
                {{ errors.expected_duration }}
              </div>
            </div>
          </div>
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="parkingDate" class="form-label">
                <i class="fas fa-calendar me-1"></i>
                Parking Date <span class="text-danger">*</span>
              </label>
              <input
                id="parkingDate"
                v-model="form.parking_date"
                type="date"
                class="form-control"
                :class="{ 'is-invalid': errors.parking_date }"
                :min="today"
                :max="maxDate"
                required
                :disabled="isLoading"
              >
              <div v-if="errors.parking_date" class="invalid-feedback">
                {{ errors.parking_date }}
              </div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="parkingTime" class="form-label">
                <i class="fas fa-clock me-1"></i>
                Parking Time <span class="text-danger">*</span>
              </label>
              <input
                id="parkingTime"
                v-model="form.parking_time"
                type="time"
                class="form-control"
                :class="{ 'is-invalid': errors.parking_time }"
                required
                :disabled="isLoading"
              >
              <div v-if="errors.parking_time" class="invalid-feedback">
                {{ errors.parking_time }}
              </div>
            </div>
          </div>
          
          <div class="mb-4">
            <label for="remarks" class="form-label">
              <i class="fas fa-comment me-1"></i>
              Special Instructions (Optional)
            </label>
            <textarea
              id="remarks"
              v-model="form.remarks"
              class="form-control"
              rows="3"
              placeholder="Any special instructions or notes..."
              :disabled="isLoading"
            ></textarea>
          </div>
          
          <div class="cost-estimate mb-4">
            <div class="estimate-header">
              <h6 class="text-primary">
                <i class="fas fa-calculator me-2"></i>Cost Estimate
              </h6>
            </div>
            <div class="estimate-body">
              <div class="estimate-row">
                <span>Base Rate (₹{{ selectedLot?.price || 0 }}/hour)</span>
                <span>₹{{ baseRate }}</span>
              </div>
              <div class="estimate-row">
                <span>Duration ({{ form.expected_duration || 0 }} hours)</span>
                <span>{{ form.expected_duration || 0 }}h</span>
              </div>
              <div v-if="discountAmount > 0" class="estimate-row discount">
                <span>Discount (Early Bird)</span>
                <span>-₹{{ discountAmount }}</span>
              </div>
              <hr>
              <div class="estimate-row total">
                <span class="fw-bold">Estimated Total</span>
                <span class="fw-bold text-primary">₹{{ estimatedCost }}</span>
              </div>
              <small class="text-muted">
                <i class="fas fa-info-circle me-1"></i>
                Final cost may vary based on actual duration
              </small>
            </div>
          </div>
          
          <div class="terms-section mb-4">
            <div class="form-check">
              <input
                id="agreeTerms"
                v-model="form.agree_terms"
                type="checkbox"
                class="form-check-input"
                :class="{ 'is-invalid': errors.agree_terms }"
                required
                :disabled="isLoading"
              >
              <label for="agreeTerms" class="form-check-label">
                I agree to the <a href="#" @click="showTerms">Terms and Conditions</a>
                and <a href="#" @click="showCancellation">Cancellation Policy</a>
                <span class="text-danger">*</span>
              </label>
              <div v-if="errors.agree_terms" class="invalid-feedback d-block">
                {{ errors.agree_terms }}
              </div>
            </div>
          </div>
          
          <div class="d-flex justify-content-between align-items-center">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="$emit('back-to-selection')"
              :disabled="isLoading"
            >
              <i class="fas fa-arrow-left me-1"></i>Back to Selection
            </button>
            <div class="d-flex gap-2">
              <button
                type="button"
                class="btn btn-secondary"
                @click="saveAsDraft"
                :disabled="isLoading"
              >
                <i class="fas fa-save me-1"></i>Save Draft
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isLoading || !isFormValid"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-check me-1"></i>
                {{ isLoading ? 'Booking...' : 'Confirm Booking' }}
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
              Booking Confirmed!
            </h5>
          </div>
          <div class="modal-body text-center">
            <div class="success-icon mb-3">
              <i class="fas fa-parking text-success"></i>
            </div>
            <h5>Your parking spot has been reserved!</h5>
            <p class="text-muted">Booking ID: <strong>#{{ bookingId }}</strong></p>
            <div class="booking-summary">
              <div class="summary-row">
                <span>Location:</span>
                <span>{{ selectedLot.prime_location_name }}</span>
              </div>
              <div class="summary-row">
                <span>Vehicle:</span>
                <span>{{ form.vehicle_number }}</span>
              </div>
              <div class="summary-row">
                <span>Date & Time:</span>
                <span>{{ formatBookingDateTime() }}</span>
              </div>
              <div class="summary-row">
                <span>Duration:</span>
                <span>{{ form.expected_duration }} hours</span>
              </div>
              <div class="summary-row total">
                <span>Total Cost:</span>
                <span>₹{{ estimatedCost }}</span>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" @click="goToDashboard">
              <i class="fas fa-tachometer-alt me-1"></i>Go to Dashboard
            </button>
            <button type="button" class="btn btn-outline-primary" @click="bookAnother">
              <i class="fas fa-plus me-1"></i>Book Another
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showConfirmation" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useParkingStore } from '../../store/modules/parking'
export default {
  name: 'SpotBooking',
  props: {
    selectedLot: {
      type: Object,
      default: null
    }
  },
  emits: ['back-to-selection'],
  setup(props, { emit }) {
    const router = useRouter()
    const parkingStore = useParkingStore()
    const isLoading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const showConfirmation = ref(false)
    const bookingId = ref('')
    const form = reactive({
      vehicle_number: '',
      expected_duration: '',
      parking_date: '',
      parking_time: '',
      remarks: '',
      agree_terms: false
    })
    const errors = reactive({
      vehicle_number: '',
      expected_duration: '',
      parking_date: '',
      parking_time: '',
      agree_terms: ''
    })
    const today = computed(() => {
      return new Date().toISOString().split('T')[0]
    })
    const maxDate = computed(() => {
      const date = new Date()
      date.setDate(date.getDate() + 30)
      return date.toISOString().split('T')[0]
    })
    const baseRate = computed(() => {
      return (props.selectedLot?.price || 0) * (form.expected_duration || 0)
    })
    const discountAmount = computed(() => {
      if (form.parking_date && form.parking_date > today.value) {
        return Math.round(baseRate.value * 0.1)
      }
      return 0
    })
    const estimatedCost = computed(() => {
      return Math.max(0, baseRate.value - discountAmount.value)
    })
    const isFormValid = computed(() => {
      return form.vehicle_number &&
             form.expected_duration &&
             form.parking_date &&
             form.parking_time &&
             form.agree_terms &&
             !Object.values(errors).some(error => error)
    })
    const validateVehicleNumber = () => {
      const vehiclePattern = /^[A-Z]{2}[-\s]?\d{1,2}[-\s]?[A-Z]{1,2}[-\s]?\d{1,4}$/i
      if (!form.vehicle_number) {
        errors.vehicle_number = 'Vehicle number is required'
      } else if (!vehiclePattern.test(form.vehicle_number.replace(/\s/g, ''))) {
        errors.vehicle_number = 'Please enter a valid vehicle number (e.g., KA-01-AB-1234)'
      } else {
        errors.vehicle_number = ''
      }
    }
    const calculateEstimatedCost = () => {
    }
    const validateForm = () => {
      Object.keys(errors).forEach(key => errors[key] = '')
      validateVehicleNumber()
      if (!form.expected_duration) {
        errors.expected_duration = 'Please select expected duration'
      }
      if (!form.parking_date) {
        errors.parking_date = 'Please select parking date'
      } else if (form.parking_date < today.value) {
        errors.parking_date = 'Parking date cannot be in the past'
      }
      if (!form.parking_time) {
        errors.parking_time = 'Please select parking time'
      }
      if (!form.agree_terms) {
        errors.agree_terms = 'You must agree to the terms and conditions'
      }
      return Object.values(errors).every(error => !error)
    }
    const handleBooking = async () => {
      if (!validateForm()) return
      isLoading.value = true
      error.value = ''
      successMessage.value = ''
      try {
        const bookingData = {
          lot_id: props.selectedLot.id,
          vehicle_number: form.vehicle_number.toUpperCase(),
          expected_duration: parseInt(form.expected_duration),
          parking_datetime: `${form.parking_date}T${form.parking_time}`,
          remarks: form.remarks,
          estimated_cost: estimatedCost.value
        }
        const result = await parkingStore.bookParkingSpot(bookingData)
        if (result.success) {
          bookingId.value = result.booking_id
          showConfirmation.value = true
          successMessage.value = 'Parking spot booked successfully!'
        }
      } catch (err) {
        error.value = err.message || 'Booking failed. Please try again.'
      } finally {
        isLoading.value = false
      }
    }
    const saveAsDraft = () => {
      const draftData = { ...form, lot_id: props.selectedLot?.id }
      localStorage.setItem('parking_booking_draft', JSON.stringify(draftData))
      successMessage.value = 'Draft saved successfully!'
    }
    const loadDraft = () => {
      const draft = localStorage.getItem('parking_booking_draft')
      if (draft) {
        const draftData = JSON.parse(draft)
        if (draftData.lot_id === props.selectedLot?.id) {
          Object.keys(form).forEach(key => {
            if (draftData[key]) {
              form[key] = draftData[key]
            }
          })
        }
      }
    }
    const formatBookingDateTime = () => {
      if (!form.parking_date || !form.parking_time) return ''
      const date = new Date(`${form.parking_date}T${form.parking_time}`)
      return date.toLocaleString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    const changeLocation = () => {
      emit('back-to-selection')
    }
    const showTerms = () => {
      alert('Terms and Conditions will be displayed here')
    }
    const showCancellation = () => {
      alert('Cancellation Policy will be displayed here')
    }
    const goToDashboard = () => {
      showConfirmation.value = false
      router.push('/user/dashboard')
    }
    const bookAnother = () => {
      showConfirmation.value = false
      Object.keys(form).forEach(key => {
        form[key] = key === 'agree_terms' ? false : ''
      })
      error.value = ''
      successMessage.value = ''
    }
    onMounted(() => {
      form.parking_date = today.value
      form.parking_time = new Date().toTimeString().slice(0, 5)
      loadDraft()
    })
    return {
      isLoading,
      error,
      successMessage,
      showConfirmation,
      bookingId,
      form,
      errors,
      today,
      maxDate,
      baseRate,
      discountAmount,
      estimatedCost,
      isFormValid,
      validateVehicleNumber,
      calculateEstimatedCost,
      handleBooking,
      saveAsDraft,
      formatBookingDateTime,
      changeLocation,
      showTerms,
      showCancellation,
      goToDashboard,
      bookAnother
    }
  }
}
</script>
<style scoped>
.spot-booking {
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
.btn-secondary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-primary, .btn-outline-secondary {
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
.location-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.location-card .card-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  border-radius: 15px 15px 0 0 !important;
}
.location-name {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.location-address {
  color: #6c757d;
  margin-bottom: 1rem;
}
.location-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}
.meta-item {
  background: rgba(138, 184, 254, 0.1);
  color: var(--secondary-color);
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
}
.availability-circle {
  width: 100px;
  height: 100px;
  border: 4px solid var(--text-accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
}
.circle-content h3 {
  color: var(--primary-color);
  font-weight: 700;
  margin: 0;
}
.circle-content small {
  color: var(--secondary-color);
  font-weight: 600;
}
.booking-form-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.booking-form-card .card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 15px 15px 0 0 !important;
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
.cost-estimate {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid rgba(138, 184, 254, 0.2);
}
.estimate-header h6 {
  margin-bottom: 1rem;
}
.estimate-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}
.estimate-row.discount {
  color: #28a745;
  font-weight: 600;
}
.estimate-row.total {
  font-size: 1.1rem;
  color: var(--primary-color);
}
.terms-section {
  background: rgba(138, 184, 254, 0.05);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid rgba(138, 184, 254, 0.2);
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
.booking-summary {
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
.summary-row.total {
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--primary-color);
  border-top: 1px solid rgba(138, 184, 254, 0.3);
  padding-top: 0.5rem;
  margin-top: 0.5rem;
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
  .location-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  .meta-item {
    text-align: center;
  }
  .availability-circle {
    width: 80px;
    height: 80px;
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