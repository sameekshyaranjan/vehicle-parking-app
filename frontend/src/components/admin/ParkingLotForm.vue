<template>
  <div class="parking-lot-form">
    <div class="card form-card">
      <div class="card-header">
        <h5 class="card-title mb-0">
          <i class="fas fa-building me-2"></i>
          {{ isEditing ? 'Edit Parking Lot' : 'Create New Parking Lot' }}
        </h5>
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
        <form @submit.prevent="handleSubmit">
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="locationName" class="form-label">
                <i class="fas fa-map-marker-alt me-1"></i>
                Prime Location Name <span class="text-danger">*</span>
              </label>
              <input
                id="locationName"
                v-model="form.prime_location_name"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.prime_location_name }"
                placeholder="Enter location name"
                required
                :disabled="isLoading"
              >
              <div v-if="errors.prime_location_name" class="invalid-feedback">
                {{ errors.prime_location_name }}
              </div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="price" class="form-label">
                <i class="fas fa-rupee-sign me-1"></i>
                Price per Hour <span class="text-danger">*</span>
              </label>
              <div class="input-group">
                <span class="input-group-text">₹</span>
                <input
                  id="price"
                  v-model.number="form.price"
                  type="number"
                  class="form-control"
                  :class="{ 'is-invalid': errors.price }"
                  placeholder="0.00"
                  min="0"
                  step="0.01"
                  required
                  :disabled="isLoading"
                >
                <div v-if="errors.price" class="invalid-feedback">
                  {{ errors.price }}
                </div>
              </div>
            </div>
          </div>
          
          <div class="mb-3">
            <label for="address" class="form-label">
              <i class="fas fa-home me-1"></i>
              Address <span class="text-danger">*</span>
            </label>
            <textarea
              id="address"
              v-model="form.address"
              class="form-control"
              :class="{ 'is-invalid': errors.address }"
              placeholder="Enter complete address"
              rows="3"
              required
              :disabled="isLoading"
            ></textarea>
            <div v-if="errors.address" class="invalid-feedback">
              {{ errors.address }}
            </div>
          </div>
          <div class="row">
            
            <div class="col-md-6 mb-3">
              <label for="pinCode" class="form-label">
                <i class="fas fa-map-pin me-1"></i>
                PIN Code <span class="text-danger">*</span>
              </label>
              <input
                id="pinCode"
                v-model="form.pin_code"
                type="text"
                class="form-control"
                :class="{ 'is-invalid': errors.pin_code }"
                placeholder="Enter 6-digit PIN"
                maxlength="6"
                required
                :disabled="isLoading"
              >
              <div v-if="errors.pin_code" class="invalid-feedback">
                {{ errors.pin_code }}
              </div>
            </div>
            
            <div class="col-md-6 mb-3">
              <label for="numberOfSpots" class="form-label">
                <i class="fas fa-car me-1"></i>
                Number of Parking Spots <span class="text-danger">*</span>
              </label>
              <input
                id="numberOfSpots"
                v-model.number="form.number_of_spots"
                type="number"
                class="form-control"
                :class="{ 'is-invalid': errors.number_of_spots }"
                placeholder="Enter number of spots"
                min="1"
                max="1000"
                required
                :disabled="isLoading"
              >
              <div v-if="errors.number_of_spots" class="invalid-feedback">
                {{ errors.number_of_spots }}
              </div>
              <div class="form-text">Maximum 1000 spots per lot</div>
            </div>
          </div>
          
          <div class="d-flex justify-content-between align-items-center">
            <button
              type="button"
              class="btn btn-outline-secondary"
              @click="resetForm"
              :disabled="isLoading"
            >
              <i class="fas fa-undo me-1"></i>Reset
            </button>
            <div class="d-flex gap-2">
              <button
                type="button"
                class="btn btn-secondary"
                @click="$emit('cancel')"
                :disabled="isLoading"
              >
                <i class="fas fa-times me-1"></i>Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isLoading || !isFormValid"
              >
                <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else :class="isEditing ? 'fas fa-save' : 'fas fa-plus'" class="me-1"></i>
                {{ isLoading ? 'Saving...' : (isEditing ? 'Update Lot' : 'Create Lot') }}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
export default {
  name: 'ParkingLotForm',
  props: {
    editData: {
      type: Object,
      default: null
    }
  },
  emits: ['success', 'cancel'],
  setup(props, { emit }) {
    const adminStore = useAdminStore()
    const isLoading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const form = reactive({
      prime_location_name: '',
      price: 0,
      address: '',
      pin_code: '',
      number_of_spots: 1
    })
    const errors = reactive({
      prime_location_name: '',
      price: '',
      address: '',
      pin_code: '',
      number_of_spots: ''
    })
    const isEditing = computed(() => !!props.editData)
    const isFormValid = computed(() => {
      return form.prime_location_name &&
             form.price > 0 &&
             form.address &&
             form.pin_code &&
             form.number_of_spots > 0 &&
             !Object.values(errors).some(error => error)
    })
    const validateForm = () => {
      Object.keys(errors).forEach(key => errors[key] = '')
      if (!form.prime_location_name.trim()) {
        errors.prime_location_name = 'Location name is required'
      }
      if (!form.price || form.price <= 0) {
        errors.price = 'Price must be greater than 0'
      }
      if (!form.address.trim()) {
        errors.address = 'Address is required'
      }
      if (!form.pin_code || !/^\d{6}$/.test(form.pin_code)) {
        errors.pin_code = 'PIN code must be 6 digits'
      }
      if (!form.number_of_spots || form.number_of_spots < 1 || form.number_of_spots > 1000) {
        errors.number_of_spots = 'Number of spots must be between 1 and 1000'
      }
      return Object.values(errors).every(error => !error)
    }
    const handleSubmit = async () => {
      if (!validateForm()) return
      isLoading.value = true
      error.value = ''
      successMessage.value = ''
      try {
        if (isEditing.value) {
          await adminStore.updateParkingLot(props.editData.id, form)
          successMessage.value = 'Parking lot updated successfully!'
        } else {
          await adminStore.createParkingLot(form)
          successMessage.value = 'Parking lot created successfully!'
        }
        setTimeout(() => {
          emit('success')
        }, 1500)
      } catch (err) {
        error.value = err.message || 'An error occurred'
      } finally {
        isLoading.value = false
      }
    }
    const resetForm = () => {
      if (props.editData) {
        populateForm()
      } else {
        Object.keys(form).forEach(key => {
          if (key === 'price' || key === 'number_of_spots') {
            form[key] = key === 'number_of_spots' ? 1 : 0
          } else {
            form[key] = ''
          }
        })
      }
      Object.keys(errors).forEach(key => errors[key] = '')
      error.value = ''
      successMessage.value = ''
    }
    const populateForm = () => {
      if (props.editData) {
        Object.keys(form).forEach(key => {
          form[key] = props.editData[key] || (key === 'number_of_spots' ? 1 : '')
        })
      }
    }
    watch(() => props.editData, () => {
      populateForm()
    }, { immediate: true })
    onMounted(() => {
      populateForm()
    })
    return {
      form,
      errors,
      isLoading,
      error,
      successMessage,
      isEditing,
      isFormValid,
      handleSubmit,
      resetForm
    }
  }
}
</script>
<style scoped>
.parking-lot-form {
  max-width: 800px;
  margin: 0 auto;
}
.form-card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 1, 51, 0.1);
}
.card-header {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: var(--text-accent);
  border-radius: 15px 15px 0 0 !important;
  padding: 1.5rem;
}
.card-title {
  font-weight: 600;
  margin: 0;
}
.form-label {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.form-control {
  border: 2px solid rgba(138, 184, 254, 0.3);
  border-radius: 8px;
  padding: 0.75rem;
  transition: all 0.3s ease;
}
.form-control:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(75, 0, 110, 0.4);
}
.btn-secondary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}
.btn-outline-secondary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
  border-radius: 8px;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
}
.btn-outline-secondary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.input-group-text {
  background-color: rgba(138, 184, 254, 0.1);
  border-color: rgba(138, 184, 254, 0.3);
  color: var(--secondary-color);
  font-weight: 600;
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
.text-danger {
  color: #dc3545 !important;
}
.form-text {
  font-size: 0.875rem;
  color: #6c757d;
}
.gap-2 {
  gap: 0.5rem;
}
@media (max-width: 768px) {
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