<template>
  <div class="parking-spot-grid">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary mb-1">
          <i class="fas fa-th-large me-2"></i>{{ lotName }} - Parking Spots
        </h4>
        <p class="text-muted mb-0">{{ totalSpots }} spots • {{ occupiedSpots }} occupied • {{ availableSpots }} available</p>
      </div>
      <button class="btn btn-outline-primary" @click="$emit('back')">
        <i class="fas fa-arrow-left me-1"></i>Back to Lots
      </button>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="quick-stat">
          <div class="stat-icon bg-primary">
            <i class="fas fa-car"></i>
          </div>
          <div class="stat-info">
            <h6>Total Spots</h6>
            <h4>{{ totalSpots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="quick-stat">
          <div class="stat-icon bg-success">
            <i class="fas fa-check-circle"></i>
          </div>
          <div class="stat-info">
            <h6>Available</h6>
            <h4>{{ availableSpots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="quick-stat">
          <div class="stat-icon bg-danger">
            <i class="fas fa-times-circle"></i>
          </div>
          <div class="stat-info">
            <h6>Occupied</h6>
            <h4>{{ occupiedSpots }}</h4>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="quick-stat">
          <div class="stat-icon bg-info">
            <i class="fas fa-percentage"></i>
          </div>
          <div class="stat-info">
            <h6>Occupancy</h6>
            <h4>{{ occupancyRate }}%</h4>
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
                placeholder="Search by spot number..."
              >
            </div>
          </div>
          <div class="col-md-4">
            <select v-model="filterStatus" class="form-select">
              <option value="">All Spots</option>
              <option value="A">Available Only</option>
              <option value="O">Occupied Only</option>
            </select>
          </div>
          <div class="col-md-4">
            <div class="view-toggle">
              <div class="btn-group" role="group">
                <input
                  type="radio"
                  class="btn-check"
                  id="gridView"
                  :checked="viewMode === 'grid'"
                  @change="viewMode = 'grid'"
                >
                <label class="btn btn-outline-primary" for="gridView">
                  <i class="fas fa-th"></i> Grid
                </label>
                <input
                  type="radio"
                  class="btn-check"
                  id="listView"
                  :checked="viewMode === 'list'"
                  @change="viewMode = 'list'"
                >
                <label class="btn btn-outline-primary" for="listView">
                  <i class="fas fa-list"></i> List
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
      <p class="mt-2 text-muted">Loading parking spots...</p>
    </div>
    
    <div v-else-if="viewMode === 'grid'" class="spots-grid">
      <div v-if="filteredSpots.length === 0" class="empty-state">
        <i class="fas fa-search text-muted"></i>
        <h5>No spots found</h5>
        <p class="text-muted">Try adjusting your search criteria</p>
      </div>
      <div v-else class="spots-container">
        <div
          v-for="spot in filteredSpots"
          :key="spot.id"
          class="spot-card"
          :class="getSpotClass(spot)"
          @click="selectSpot(spot)"
        >
          <div class="spot-number">{{ spot.spot_number }}</div>
          <div class="spot-status">
            <i class="fas" :class="getStatusIcon(spot.status)"></i>
          </div>
          <div v-if="spot.status === 'O'" class="spot-details">
            <small class="vehicle-info">{{ spot.vehicle_number || 'Unknown' }}</small>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else-if="viewMode === 'list'" class="spots-list">
      <div v-if="filteredSpots.length === 0" class="empty-state">
        <i class="fas fa-search text-muted"></i>
        <h5>No spots found</h5>
        <p class="text-muted">Try adjusting your search criteria</p>
      </div>
      <div v-else class="table-responsive">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Spot #</th>
              <th>Status</th>
              <th>Vehicle Number</th>
              <th>User</th>
              <th>Parked Since</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="spot in filteredSpots" :key="spot.id">
              <td>
                <span class="fw-bold text-primary">{{ spot.spot_number }}</span>
              </td>
              <td>
                <span class="status-badge" :class="getStatusBadgeClass(spot.status)">
                  <i class="fas" :class="getStatusIcon(spot.status)"></i>
                  {{ spot.status === 'A' ? 'Available' : 'Occupied' }}
                </span>
              </td>
              <td>
                {{ spot.vehicle_number || '-' }}
              </td>
              <td>
                {{ spot.user_name || '-' }}
              </td>
              <td>
                {{ spot.parking_since ? formatDateTime(spot.parking_since) : '-' }}
              </td>
              <td>
                <button
                  class="btn btn-sm btn-outline-primary me-1"
                  @click="viewSpotDetails(spot)"
                >
                  <i class="fas fa-eye"></i>
                </button>
                <button
                  v-if="spot.status === 'O'"
                  class="btn btn-sm btn-outline-warning"
                  @click="releaseSpot(spot)"
                >
                  <i class="fas fa-unlock"></i>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div v-if="selectedSpot" class="modal d-block">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-car me-2"></i>
              Spot #{{ selectedSpot.spot_number }} Details
            </h5>
            <button type="button" class="btn-close" @click="selectedSpot = null"></button>
          </div>
          <div class="modal-body">
            <div class="row">
              <div class="col-6">
                <div class="detail-item">
                  <label>Status</label>
                  <span class="status-badge" :class="getStatusBadgeClass(selectedSpot.status)">
                    <i class="fas" :class="getStatusIcon(selectedSpot.status)"></i>
                    {{ selectedSpot.status === 'A' ? 'Available' : 'Occupied' }}
                  </span>
                </div>
              </div>
              <div class="col-6">
                <div class="detail-item">
                  <label>Spot Number</label>
                  <span class="fw-bold">{{ selectedSpot.spot_number }}</span>
                </div>
              </div>
            </div>
            <div v-if="selectedSpot.status === 'O'" class="occupied-details mt-3">
              <h6 class="text-primary">Occupation Details</h6>
              <div class="row">
                <div class="col-6">
                  <div class="detail-item">
                    <label>Vehicle Number</label>
                    <span class="fw-bold">{{ selectedSpot.vehicle_number || 'Unknown' }}</span>
                  </div>
                </div>
                <div class="col-6">
                  <div class="detail-item">
                    <label>User</label>
                    <span>{{ selectedSpot.user_name || 'Unknown' }}</span>
                  </div>
                </div>
              </div>
              <div class="row mt-2">
                <div class="col-6">
                  <div class="detail-item">
                    <label>Parked Since</label>
                    <span>{{ selectedSpot.parking_since ? formatDateTime(selectedSpot.parking_since) : 'Unknown' }}</span>
                  </div>
                </div>
                <div class="col-6">
                  <div class="detail-item">
                    <label>Duration</label>
                    <span>{{ calculateDuration(selectedSpot.parking_since) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="selectedSpot = null">
              Close
            </button>
            <button
              v-if="selectedSpot.status === 'O'"
              type="button"
              class="btn btn-warning"
              @click="releaseSpot(selectedSpot)"
            >
              <i class="fas fa-unlock me-1"></i>Release Spot
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="selectedSpot" class="modal-backdrop"></div>
  </div>
</template>
<script>
import { ref, computed, onMounted, watch } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
export default {
  name: 'ParkingSpotGrid',
  props: {
    lotId: {
      type: Number,
      required: true
    }
  },
  emits: ['back'],
  setup(props) {
    const adminStore = useAdminStore()
    const isLoading = ref(false)
    const searchQuery = ref('')
    const filterStatus = ref('')
    const viewMode = ref('grid')
    const selectedSpot = ref(null)
    const spotData = ref({ lot_name: '', spots: [] })
    const lotName = computed(() => spotData.value.lot_name)
    const totalSpots = computed(() => spotData.value.spots.length)
    const occupiedSpots = computed(() =>
      spotData.value.spots.filter(spot => spot.status === 'O').length
    )
    const availableSpots = computed(() =>
      spotData.value.spots.filter(spot => spot.status === 'A').length
    )
    const occupancyRate = computed(() =>
      totalSpots.value > 0 ? Math.round((occupiedSpots.value / totalSpots.value) * 100) : 0
    )
    const filteredSpots = computed(() => {
      let spots = [...spotData.value.spots]
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        spots = spots.filter(spot =>
          spot.spot_number.toString().includes(query) ||
          (spot.vehicle_number && spot.vehicle_number.toLowerCase().includes(query))
        )
      }
      if (filterStatus.value) {
        spots = spots.filter(spot => spot.status === filterStatus.value)
      }
      spots.sort((a, b) => a.spot_number - b.spot_number)
      return spots
    })
    const getSpotClass = (spot) => {
      return {
        'spot-available': spot.status === 'A',
        'spot-occupied': spot.status === 'O'
      }
    }
    const getStatusIcon = (status) => {
      return status === 'A' ? 'fa-check' : 'fa-times'
    }
    const getStatusBadgeClass = (status) => {
      return status === 'A' ? 'status-available' : 'status-occupied'
    }
    const selectSpot = (spot) => {
      selectedSpot.value = spot
    }
    const viewSpotDetails = (spot) => {
      selectedSpot.value = spot
    }
    const releaseSpot = async (spot) => {
      if (confirm(`Are you sure you want to release spot #${spot.spot_number}?`)) {
        console.log('Releasing spot:', spot.id)
        await loadSpots()
      }
    }
    const formatDateTime = (dateString) => {
      if (!dateString) return 'Unknown'
      return new Date(dateString).toLocaleString()
    }
    const calculateDuration = (startTime) => {
      if (!startTime) return 'Unknown'
      const start = new Date(startTime)
      const now = new Date()
      const diffMs = now - start
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      if (diffHours > 0) {
        return `${diffHours}h ${diffMins}m`
      }
      return `${diffMins}m`
    }
    const loadSpots = async () => {
      isLoading.value = true
      try {
        const data = await adminStore.fetchParkingSpots(props.lotId)
        spotData.value = data
      } catch (error) {
        console.error('Error loading spots:', error)
      } finally {
        isLoading.value = false
      }
    }
    watch(() => props.lotId, () => {
      if (props.lotId) {
        loadSpots()
      }
    }, { immediate: true })
    return {
      isLoading,
      searchQuery,
      filterStatus,
      viewMode,
      selectedSpot,
      lotName,
      totalSpots,
      occupiedSpots,
      availableSpots,
      occupancyRate,
      filteredSpots,
      getSpotClass,
      getStatusIcon,
      getStatusBadgeClass,
      selectSpot,
      viewSpotDetails,
      releaseSpot,
      formatDateTime,
      calculateDuration
    }
  }
}
</script>
<style scoped>
.parking-spot-grid {
  padding: 1rem;
}
.text-primary {
  color: var(--primary-color) !important;
}
.btn-primary, .btn-outline-primary {
  border-color: var(--secondary-color);
  color: var(--secondary-color);
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
}
.btn-outline-primary:hover {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
}
.quick-stat {
  background: white;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
}
.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  color: white;
  margin-right: 1rem;
}
.stat-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.stat-info h6 {
  color: #6c757d;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}
.stat-info h4 {
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
.spots-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 1rem;
  padding: 1rem;
}
.spot-card {
  aspect-ratio: 1;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 3px 10px rgba(0, 1, 51, 0.1);
  position: relative;
}
.spot-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.2);
}
.spot-available {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  color: #155724;
  border: 2px solid #28a745;
}
.spot-occupied {
  background: linear-gradient(135deg, #f8d7da, #f1b0b7);
  color: #721c24;
  border: 2px solid #dc3545;
}
.spot-number {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.spot-status i {
  font-size: 1rem;
}
.vehicle-info {
  position: absolute;
  bottom: 0.25rem;
  font-size: 0.7rem;
  font-weight: 600;
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
.status-occupied {
  background-color: #f8d7da;
  color: #721c24;
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
.table tbody tr:hover {
  background-color: rgba(138, 184, 254, 0.05);
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
  margin-bottom: 1rem;
}
.detail-item label {
  display: block;
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
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
.view-toggle .btn-check:checked + .btn-outline-primary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
@media (max-width: 768px) {
  .spots-container {
    grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
    gap: 0.75rem;
  }
  .spot-card {
    font-size: 0.9rem;
  }
  .quick-stat {
    margin-bottom: 1rem;
  }
  .table-responsive {
    font-size: 0.9rem;
  }
}
</style>