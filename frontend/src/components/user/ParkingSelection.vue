<template>
  <div class="parking-selection">
    
    <div class="selection-header mb-4">
      <h4 class="text-primary mb-1">
        <i class="fas fa-map-marker-alt me-2"></i>Find Parking Near You
      </h4>
      <p class="text-muted mb-0" id ="textp">Choose from available parking locations</p>
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
                placeholder="Search by location, address..."
              >
            </div>
          </div>
          <div class="col-md-2">
            <select v-model="priceFilter" class="form-select">
              <option value="">All Prices</option>
              <option value="low">Under ₹50</option>
              <option value="medium">₹50 - ₹100</option>
              <option value="high">Above ₹100</option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="sortBy" class="form-select">
              <option value="distance">Nearest First</option>
              <option value="price">Price: Low to High</option>
              <option value="availability">Most Available</option>
              <option value="rating">Highest Rated</option>
            </select>
          </div>
          <div class="col-md-2">
            <div class="form-check form-switch mt-2">
              <input
                v-model="showAvailableOnly"
                class="form-check-input"
                type="checkbox"
                id="availableOnly"
              >
              <label class="form-check-label" for="availableOnly">
                Available Only
              </label>
            </div>
          </div>
          <div class="col-md-2">
            <button class="btn btn-outline-primary w-100" @click="refreshLocations">
              <i class="fas fa-sync me-1"></i>Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-primary">
            <i class="fas fa-map"></i>
          </div>
          <div class="stats-content">
            <h6>Available Lots</h6>
            <h4>{{ availableLotsCount }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-success">
            <i class="fas fa-car"></i>
          </div>
          <div class="stats-content">
            <h6>Free Spots</h6>
            <h4>{{ totalAvailableSpots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-warning">
            <i class="fas fa-rupee-sign"></i>
          </div>
          <div class="stats-content">
            <h6>Best Price</h6>
            <h4>₹{{ bestPrice }}/hr</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-info">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stats-content">
            <h6>Avg Duration</h6>
            <h4>{{ avgDuration }}h</h4>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Finding parking locations...</p>
    </div>
    
    <div v-else-if="filteredLots.length === 0" class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-map-marker-alt"></i>
      </div>
      <h5>No Parking Locations Found</h5>
      <p class="text-muted" id ="textp">Try adjusting your search criteria or check back later</p>
      <button class="btn btn-primary" @click="refreshLocations">
        <i class="fas fa-sync me-1"></i>Refresh Locations
      </button>
    </div>
    
    <div v-else class="row">
      <div v-for="lot in filteredLots" :key="lot.id" class="col-lg-6 col-xl-4 mb-4">
        <div class="parking-lot-card" :class="{ 'selected': selectedLot?.id === lot.id }">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-start">
              <div class="lot-info">
                <h6 class="lot-name">{{ lot.prime_location_name }}</h6>
                <p class="lot-address">
                  <i class="fas fa-map-marker-alt me-1"></i>
                  {{ lot.address }}
                </p>
              </div>
              <div class="availability-badge" :class="getAvailabilityClass(lot)">
                {{ lot.available_spots }} spots
              </div>
            </div>
          </div>
          <div class="card-body">
            
            <div class="row mb-3">
              <div class="col-6">
                <div class="info-item">
                  <small class="text-muted">Price per Hour</small>
                  <div class="price">₹{{ lot.price }}</div>
                </div>
              </div>
              <div class="col-6">
                <div class="info-item">
                  <small class="text-muted">Distance</small>
                  <div class="distance">{{ lot.distance || '2.5' }} km</div>
                </div>
              </div>
            </div>
            
            <div class="features mb-3">
              <span class="feature-tag">
                <i class="fas fa-shield-alt me-1"></i>Secure
              </span>
              <span class="feature-tag">
                <i class="fas fa-camera me-1"></i>CCTV
              </span>
              <span v-if="lot.price < 50" class="feature-tag featured">
                <i class="fas fa-star me-1"></i>Budget Friendly
              </span>
            </div>
            
            <div class="occupancy-section mb-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <small class="text-muted">Occupancy</small>
                <small class="fw-bold">{{lot.total_spots - lot.available_spots }}/{{ lot.total_spots }}</small>
              </div>
              <div class="progress">
                <div
                  class="progress-bar"
                  :class="getOccupancyClass(lot)"
                  :style="{ width: getOccupancyRate(lot) + '%' }"
                ></div>
              </div>
            </div>
            
            <div class="d-flex justify-content-between align-items-center">
              <button
                class="btn btn-outline-primary btn-sm"
                @click="viewDetails(lot)"
              >
                <i class="fas fa-info-circle me-1"></i>Details
              </button>
              <button
                class="btn btn-primary"
                :disabled="!lot.is_available || hasActiveReservation"
                @click="selectLot(lot)"
              >
                <i class="fas fa-parking me-1"></i>
                {{ lot.is_available ? 'Select' : 'Full' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="detailsLot" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-building me-2"></i>
              {{ detailsLot.prime_location_name }}
            </h5>
            <button type="button" class="btn-close" @click="detailsLot = null"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-primary">Location Details</h6>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Address</label>
                    <span>{{ detailsLot.address }}</span>
                  </div>
                  <div class="detail-item">
                    <label>PIN Code</label>
                    <span>{{ detailsLot.pin_code }}</span>
                  </div>
                  <div class="detail-item">
                    <label>Distance</label>
                    <span>{{ detailsLot.distance || '2.5' }} km away</span>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <h6 class="text-primary">Availability & Pricing</h6>
                <div class="detail-grid">
                  <div class="detail-item">
                    <label>Price per Hour</label>
                    <span class="price-highlight">₹{{ detailsLot.price }}</span>
                  </div>
                  <div class="detail-item">
                    <label>Available Spots</label>
                    <span class="availability-highlight">{{ detailsLot.available_spots }}</span>
                  </div>
                  <div class="detail-item">
                    <label>Total Capacity</label>
                    <span>{{ detailsLot.total_spots }} spots</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-4">
              <h6 class="text-primary">Facilities</h6>
              <div class="facilities-grid">
                <div class="facility-item">
                  <i class="fas fa-shield-alt text-success"></i>
                  <span>24/7 Security</span>
                </div>
                <div class="facility-item">
                  <i class="fas fa-camera text-info"></i>
                  <span>CCTV Monitoring</span>
                </div>
                <div class="facility-item">
                  <i class="fas fa-lightbulb text-warning"></i>
                  <span>Well Lit</span>
                </div>
                <div class="facility-item">
                  <i class="fas fa-car text-primary"></i>
                  <span>Car Wash Available</span>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="detailsLot = null">
              Close
            </button>
            <button
              type="button"
              class="btn btn-primary"
              :disabled="!detailsLot.is_available || hasActiveReservation"
              @click="selectLot(detailsLot)"
            >
              <i class="fas fa-parking me-1"></i>Select This Location
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="detailsLot" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useParkingStore } from '../../store/modules/parking'
export default {
  name: 'ParkingSelection',
  emits: ['lot-selected'],
  setup(props, { emit }) {
    const parkingStore = useParkingStore()
    const isLoading = ref(false)
    const searchQuery = ref('')
    const priceFilter = ref('')
    const sortBy = ref('distance')
    const showAvailableOnly = ref(true)
    const selectedLot = ref(null)
    const detailsLot = ref(null)
    const availableLotsCount = computed(() => parkingStore.availableLotsCount)
    const totalAvailableSpots = computed(() => parkingStore.totalAvailableSpots)
    const hasActiveReservation = computed(() => parkingStore.hasActiveReservation)
    const bestPrice = computed(() => {
      if (parkingStore.availableLots.length === 0) return 0
      return Math.min(...parkingStore.availableLots.map(lot => lot.price))
    })
    const avgDuration = computed(() => 2.5)
    const filteredLots = computed(() => {
      let lots = [...parkingStore.availableLots]
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        lots = lots.filter(lot =>
          lot.prime_location_name.toLowerCase().includes(query) ||
          lot.address.toLowerCase().includes(query)
        )
      }
      if (priceFilter.value) {
        lots = lots.filter(lot => {
          switch (priceFilter.value) {
            case 'low':
              return lot.price < 50
            case 'medium':
              return lot.price >= 50 && lot.price <= 100
            case 'high':
              return lot.price > 100
            default:
              return true
          }
        })
      }
      if (showAvailableOnly.value) {
        lots = lots.filter(lot => lot.is_available)
      }
      lots.sort((a, b) => {
        switch (sortBy.value) {
          case 'distance':
            return (a.distance || 0) - (b.distance || 0)
          case 'price':
            return a.price - b.price
          case 'availability':
            return b.available_spots - a.available_spots
          case 'rating':
            return (b.rating || 0) - (a.rating || 0)
          default:
            return 0
        }
      })
      return lots
    })
    const getAvailabilityClass = (lot) => {
      if (lot.available_spots === 0) return 'availability-full'
      if (lot.available_spots < 5) return 'availability-low'
      return 'availability-good'
    }
    const getOccupancyClass = (lot) => {
      const rate = getOccupancyRate(lot)
      if (rate < 50) return 'bg-success'
      if (rate < 80) return 'bg-warning'
      return 'bg-danger'
    }
    const getOccupancyRate = (lot) => {
      const occupied = (lot.total_spots || lot.number_of_spots) - lot.available_spots
      return ((occupied / (lot.total_spots || lot.number_of_spots)) * 100) || 0
    }
    const selectLot = (lot) => {
      if (!lot.is_available || hasActiveReservation.value) return
      selectedLot.value = lot
      parkingStore.selectLot(lot)
      detailsLot.value = null
      emit('lot-selected', lot)
    }
    const viewDetails = (lot) => {
      detailsLot.value = lot
    }
    const refreshLocations = async () => {
      isLoading.value = true
      try {
        await parkingStore.fetchAvailableLots(true)
      } catch (error) {
        console.error('Error refreshing locations:', error)
      } finally {
        isLoading.value = false
      }
    }
    onMounted(() => {
      refreshLocations()
    })
    return {
      isLoading,
      searchQuery,
      priceFilter,
      sortBy,
      showAvailableOnly,
      selectedLot,
      detailsLot,
      availableLotsCount,
      totalAvailableSpots,
      hasActiveReservation,
      bestPrice,
      avgDuration,
      filteredLots,
      getAvailabilityClass,
      getOccupancyClass,
      getOccupancyRate,
      selectLot,
      viewDetails,
      refreshLocations
    }
  }
}
</script>
<style scoped>
.parking-selection {
  padding: 1rem;
}
.text-primary {
  color: rgb(251, 251, 117) !important;
}
#textp {
  color: rgb(111, 111, 99) !important;
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
.search-box .form-control:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
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
.parking-lot-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
  border: 2px solid transparent;
}
.parking-lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 1, 51, 0.15);
}
.parking-lot-card.selected {
  border-color: var(--secondary-color);
  box-shadow: 0 10px 25px rgba(75, 0, 110, 0.3);
}
.parking-lot-card .card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: none;
  padding: 1.25rem;
}
.lot-name {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.lot-address {
  color: #6c757d;
  font-size: 0.9rem;
  margin: 0;
}
.availability-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}
.availability-good {
  background-color: #d4edda;
  color: #155724;
}
.availability-low {
  background-color: #fff3cd;
  color: #856404;
}
.availability-full {
  background-color: #f8d7da;
  color: #721c24;
}
.info-item small {
  display: block;
  margin-bottom: 0.25rem;
}
.price {
  color: var(--secondary-color);
  font-weight: 700;
  font-size: 1.1rem;
}
.distance {
  color: var(--primary-color);
  font-weight: 600;
}
.features {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.feature-tag {
  padding: 0.25rem 0.5rem;
  background: rgba(138, 184, 254, 0.1);
  color: var(--secondary-color);
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
.feature-tag.featured {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: var(--primary-color);
}
.progress {
  height: 8px;
  border-radius: 4px;
  background-color: rgba(138, 184, 254, 0.2);
}
.progress-bar {
  border-radius: 4px;
}
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}
.empty-icon {
  font-size: 4rem;
  color: #dee2e6;
  margin-bottom: 1rem;
}
.detail-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
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
.price-highlight {
  color: var(--secondary-color);
  font-weight: 700;
  font-size: 1.1rem;
}
.availability-highlight {
  color: #28a745;
  font-weight: 700;
}
.facilities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}
.facility-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 8px;
}
.facility-item i {
  font-size: 1.25rem;
  margin-right: 0.75rem;
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
  .facilities-grid {
    grid-template-columns: 1fr;
  }
  .detail-item {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>