<template>
  <div class="parking-lot-list">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary mb-1">
          <i class="fas fa-building me-2"></i>Parking Lots Management
        </h4>
        <p class="text-muted mb-0">Manage and monitor all parking locations</p>
      </div>
      <button class="btn btn-primary" @click="showCreateForm">
        <i class="fas fa-plus me-1"></i>Add New Lot
      </button>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-primary">
            <i class="fas fa-building"></i>
          </div>
          <div class="stats-content">
            <h6>Total Lots</h6>
            <h4>{{ totalLots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-success">
            <i class="fas fa-car"></i>
          </div>
          <div class="stats-content">
            <h6>Total Spots</h6>
            <h4>{{ totalSpots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-warning">
            <i class="fas fa-clock"></i>
          </div>
          <div class="stats-content">
            <h6>Occupied</h6>
            <h4>{{ totalOccupied }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="stats-card">
          <div class="stats-icon bg-info">
            <i class="fas fa-percentage"></i>
          </div>
          <div class="stats-content">
            <h6>Occupancy</h6>
            <h4>{{ occupancyRate }}%</h4>
          </div>
        </div>
      </div>
    </div>
    
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-6">
            <div class="search-box">
              <i class="fas fa-search search-icon"></i>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Search parking lots..."
              >
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="filterStatus" class="form-select">
              <option value="">All Status</option>
              <option value="available">Available</option>
              <option value="full">Full</option>
              <option value="partial">Partially Occupied</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="sortBy" class="form-select">
              <option value="name">Sort by Name</option>
              <option value="price">Sort by Price</option>
              <option value="occupancy">Sort by Occupancy</option>
              <option value="spots">Sort by Total Spots</option>
            </select>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2 text-muted">Loading parking lots...</p>
    </div>
    <div v-else-if="filteredLots.length === 0" class="empty-state">
      <div class="empty-icon">
        <i class="fas fa-search"></i>
      </div>
      <h5>No Parking Lots Found</h5>
      <p class="text-muted">{{ searchQuery ? 'Try adjusting your search criteria' : 'Create your first parking lot to get started' }}</p>
      <button v-if="!searchQuery" class="btn btn-primary" @click="showCreateForm">
        <i class="fas fa-plus me-1"></i>Create First Lot
      </button>
    </div>
    <div v-else class="row">
      <div v-for="lot in filteredLots" :key="lot.id" class="col-lg-6 col-xl-4 mb-4">
        <div class="parking-lot-card">
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h6 class="lot-name">{{ lot.prime_location_name }}</h6>
                <p class="lot-address">
                  <i class="fas fa-map-marker-alt me-1"></i>
                  {{ lot.address }}
                </p>
              </div>
              <div class="dropdown">
                <button
                  class="btn btn-sm btn-outline-secondary"
                  type="button"
                  data-bs-toggle="dropdown"
                >
                  <i class="fas fa-ellipsis-v"></i>
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="#" @click="editLot(lot)">
                      <i class="fas fa-edit me-2"></i>Edit
                    </a>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li>
                    <a class="dropdown-item text-danger" href="#" @click="deleteLot(lot)">
                      <i class="fas fa-trash me-2"></i>Delete
                    </a>
                  </li>
                </ul>
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
                  <small class="text-muted">PIN Code</small>
                  <div class="pin-code">{{ lot.pin_code }}</div>
                </div>
              </div>
            </div>
            
            <div class="occupancy-section mb-3">
              <div class="d-flex justify-content-between align-items-center mb-2">
                <small class="text-muted">Occupancy</small>
                <small class="fw-bold">{{ lot.occupied_spots }}/{{ lot.number_of_spots }}</small>
              </div>
              <div class="progress">
                <div
                  class="progress-bar"
                  :class="getOccupancyClass(lot.occupancy_rate)"
                  :style="{ width: lot.occupancy_rate + '%' }"
                ></div>
              </div>
              <small class="text-muted">{{ lot.occupancy_rate }}% occupied</small>
            </div>
            
            <div class="d-flex justify-content-between align-items-center">
              <span class="status-badge" :class="getStatusClass(lot)">
                <i class="fas" :class="getStatusIcon(lot)"></i>
                {{ getStatusText(lot) }}
              </span>
              <small class="text-muted">{{ lot.available_spots }} available</small>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showModal" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <ParkingLotForm
            :edit-data="editingLot"
            @success="handleFormSuccess"
            @cancel="hideModal"
          />
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
import ParkingLotForm from './ParkingLotForm.vue'
export default {
  name: 'ParkingLotList',
  components: {
    ParkingLotForm
  },
  setup() {
    const adminStore = useAdminStore()
    const isLoading = ref(false)
    const searchQuery = ref('')
    const filterStatus = ref('')
    const sortBy = ref('name')
    const showModal = ref(false)
    const editingLot = ref(null)
    const totalLots = computed(() => adminStore.parkingLots.length)
    const totalSpots = computed(() =>
      adminStore.parkingLots.reduce((sum, lot) => sum + lot.number_of_spots, 0)
    )
    const totalOccupied = computed(() =>
      adminStore.parkingLots.reduce((sum, lot) => sum + lot.occupied_spots, 0)
    )
    const occupancyRate = computed(() =>
      totalSpots.value > 0 ? Math.round((totalOccupied.value / totalSpots.value) * 100) : 0
    )
    const filteredLots = computed(() => {
      let lots = [...adminStore.parkingLots]
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        lots = lots.filter(lot =>
          lot.prime_location_name.toLowerCase().includes(query) ||
          lot.address.toLowerCase().includes(query) ||
          lot.pin_code.includes(query)
        )
      }
      if (filterStatus.value) {
        lots = lots.filter(lot => {
          const status = getStatusValue(lot)
          return status === filterStatus.value
        })
      }
      lots.sort((a, b) => {
        switch (sortBy.value) {
          case 'name':
            return a.prime_location_name.localeCompare(b.prime_location_name)
          case 'price':
            return a.price - b.price
          case 'occupancy':
            return b.occupancy_rate - a.occupancy_rate
          case 'spots':
            return b.number_of_spots - a.number_of_spots
          default:
            return 0
        }
      })
      return lots
    })
    const getStatusValue = (lot) => {
      if (lot.available_spots === 0) return 'full'
      if (lot.occupied_spots === 0) return 'available'
      return 'partial'
    }
    const getStatusClass = (lot) => {
      const status = getStatusValue(lot)
      return {
        'status-available': status === 'available',
        'status-partial': status === 'partial',
        'status-full': status === 'full'
      }
    }
    const getStatusIcon = (lot) => {
      const status = getStatusValue(lot)
      return {
        'fa-check-circle': status === 'available',
        'fa-clock': status === 'partial',
        'fa-times-circle': status === 'full'
      }
    }
    const getStatusText = (lot) => {
      const status = getStatusValue(lot)
      return {
        'available': 'Available',
        'partial': 'Partially Occupied',
        'full': 'Full'
      }[status]
    }
    const getOccupancyClass = (rate) => {
      if (rate < 50) return 'bg-success'
      if (rate < 80) return 'bg-warning'
      return 'bg-danger'
    }
    const showCreateForm = () => {
      editingLot.value = null
      showModal.value = true
    }
    const editLot = (lot) => {
      editingLot.value = lot
      showModal.value = true
    }
    const viewSpots = (lot) => {
      console.log('View spots for lot:', lot.id)
    }
    const deleteLot = async (lot) => {
      if (confirm(`Are you sure you want to delete "${lot.prime_location_name}"?`)) {
        try {
          await adminStore.deleteParkingLot(lot.id)
        } catch (error) {
          alert('Error deleting parking lot: ' + error.message)
        }
      }
    }
    const hideModal = () => {
      showModal.value = false
      editingLot.value = null
    }
    const handleFormSuccess = () => {
      hideModal()
      loadData()
    }
    const loadData = async () => {
      isLoading.value = true
      try {
        await adminStore.fetchParkingLots()
      } catch (error) {
        console.error('Error loading parking lots:', error)
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
      showModal,
      editingLot,
      totalLots,
      totalSpots,
      totalOccupied,
      occupancyRate,
      filteredLots,
      getStatusClass,
      getStatusIcon,
      getStatusText,
      getOccupancyClass,
      showCreateForm,
      editLot,
      viewSpots,
      deleteLot,
      hideModal,
      handleFormSuccess
    }
  }
}
</script>
<style scoped>
.parking-lot-list {
  padding: 1rem;
}
.text-primary {
  color: #80ffe5 !important;
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
.search-box .form-control:focus {
  border-color: var(--secondary-color);
  box-shadow: 0 0 0 0.2rem rgba(75, 0, 110, 0.25);
}
.parking-lot-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  transition: all 0.3s ease;
  overflow: hidden;
}
.parking-lot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 1, 51, 0.15);
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
.info-item small {
  display: block;
  margin-bottom: 0.25rem;
}
.price {
  color: var(--secondary-color);
  font-weight: 700;
  font-size: 1.1rem;
}
.pin-code {
  color: var(--primary-color);
  font-weight: 600;
}
.progress {
  height: 8px;
  border-radius: 4px;
  background-color: rgba(138, 184, 254, 0.2);
}
.progress-bar {
  border-radius: 4px;
}
.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}
.status-available {
  background-color: #d4edda;
  color: #155724;
}
.status-partial {
  background-color: #fff3cd;
  color: #856404;
}
.status-full {
  background-color: #f8d7da;
  color: #721c24;
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
  .d-flex.justify-content-between {
    flex-direction: column;
    gap: 1rem;
  }
  .row .col-md-3,
  .row .col-md-6 {
    margin-bottom: 1rem;
  }
}
</style>