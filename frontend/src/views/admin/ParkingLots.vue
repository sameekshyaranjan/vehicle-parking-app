<template>
  <div class="admin-parking-lots">
    
    
    
    
    
    <div class="main-content">
      
      <ParkingLotList
        :filter-tab="activeTab"
        @lot-selected="handleLotSelected"
        @lot-edited="handleLotEdited"
        @show-spots="handleShowSpots"
      />
    </div>
    
    <div v-if="showCreateModal" class="modal d-block">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-plus me-2"></i>
              {{ editingLot ? 'Edit Parking Lot' : 'Create New Parking Lot' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <ParkingLotForm
              :edit-data="editingLot"
              @success="handleFormSuccess"
              @cancel="closeModal"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="showCreateModal" class="modal-backdrop"></div>
    
    <div v-if="showSpotsModal" class="modal d-block">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-th-large me-2"></i>
              Parking Spots - {{ selectedLot?.prime_location_name }}
            </h5>
            <button type="button" class="btn-close" @click="closeSpotsModal"></button>
          </div>
          <div class="modal-body">
            <ParkingSpotGrid
              v-if="selectedLot"
              :lot-id="selectedLot.id"
              @back="closeSpotsModal"
            />
          </div>
        </div>
      </div>
    </div>
    <div v-if="showSpotsModal" class="modal-backdrop"></div>
    
    <div v-if="selectedLots.length > 0" class="bulk-actions-panel">
      <div class="card">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-md-6">
              <span class="bulk-count">
                <i class="fas fa-check-square me-2"></i>
                {{ selectedLots.length }} lot{{ selectedLots.length > 1 ? 's' : '' }} selected
              </span>
            </div>
            <div class="col-md-6 text-md-end">
              <div class="bulk-actions">
                <button class="btn btn-outline-warning me-2" @click="bulkMaintenance">
                  <i class="fas fa-tools me-1"></i>Set Maintenance
                </button>
                <button class="btn btn-outline-success me-2" @click="bulkActivate">
                  <i class="fas fa-play me-1"></i>Activate
                </button>
                <button class="btn btn-outline-danger" @click="bulkDelete">
                  <i class="fas fa-trash me-1"></i>Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
import ParkingLotList from '../../components/admin/ParkingLotList.vue'
import ParkingLotForm from '../../components/admin/ParkingLotForm.vue'
import ParkingSpotGrid from '../../components/admin/ParkingSpotGrid.vue'
export default {
  name: 'AdminParkingLots',
  components: {
    ParkingLotList,
    ParkingLotForm,
    ParkingSpotGrid
  },
  setup() {
    const adminStore = useAdminStore()
    const activeTab = ref('all')
    const showCreateModal = ref(false)
    const showSpotsModal = ref(false)
    const editingLot = ref(null)
    const selectedLot = ref(null)
    const selectedLots = ref([])
    const allLotsCount = computed(() => adminStore.parkingLots.length)
    const availableLotsCount = computed(() =>
      adminStore.parkingLots.filter(lot => lot.available_spots > 0).length
    )
    const fullLotsCount = computed(() =>
      adminStore.parkingLots.filter(lot => lot.available_spots === 0).length
    )
    const maintenanceLotsCount = computed(() =>
      adminStore.parkingLots.filter(lot => lot.status === 'maintenance').length
    )
    const setActiveTab = (tab) => {
      activeTab.value = tab
    }
    const handleLotSelected = (lot) => {
      selectedLot.value = lot
    }
    const handleLotEdited = (lot) => {
      editingLot.value = lot
      showCreateModal.value = true
    }
    const handleShowSpots = (lot) => {
      selectedLot.value = lot
      showSpotsModal.value = true
    }
    const closeModal = () => {
      showCreateModal.value = false
      editingLot.value = null
    }
    const closeSpotsModal = () => {
      showSpotsModal.value = false
      selectedLot.value = null
    }
    const handleFormSuccess = () => {
      closeModal()
      adminStore.fetchParkingLots()
    }
    const exportData = () => {
      console.log('Exporting parking lots data...')
    }
    const bulkMaintenance = () => {
      if (confirm(`Set ${selectedLots.value.length} lots to maintenance mode?`)) {
        console.log('Setting lots to maintenance:', selectedLots.value)
        selectedLots.value = []
      }
    }
    const bulkActivate = () => {
      if (confirm(`Activate ${selectedLots.value.length} lots?`)) {
        console.log('Activating lots:', selectedLots.value)
        selectedLots.value = []
      }
    }
    const bulkDelete = () => {
      if (confirm(`Are you sure you want to delete ${selectedLots.value.length} lots? This action cannot be undone.`)) {
        console.log('Deleting lots:', selectedLots.value)
        selectedLots.value = []
      }
    }
    onMounted(() => {
      adminStore.fetchParkingLots()
    })
    return {
      activeTab,
      showCreateModal,
      showSpotsModal,
      editingLot,
      selectedLot,
      selectedLots,
      allLotsCount,
      availableLotsCount,
      fullLotsCount,
      maintenanceLotsCount,
      setActiveTab,
      handleLotSelected,
      handleLotEdited,
      handleShowSpots,
      closeModal,
      closeSpotsModal,
      handleFormSuccess,
      exportData,
      bulkMaintenance,
      bulkActivate,
      bulkDelete
    }
  }
}
</script>
<style scoped>
.admin-parking-lots {
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
.modal-title {
  font-weight: 600;
}
.bulk-actions-panel {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  width: 90%;
  max-width: 800px;
}
.bulk-actions-panel .card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 1, 51, 0.2);
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.95), rgba(255, 255, 255, 0.95));
  backdrop-filter: blur(10px);
}
.bulk-count {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 1.1rem;
}
.bulk-actions .btn {
  border-radius: 8px;
  font-weight: 600;
}
.btn-outline-warning {
  border-color: #ffc107;
  color: #ffc107;
}
.btn-outline-warning:hover {
  background-color: #ffc107;
  border-color: #ffc107;
  color: #000;
}
.btn-outline-success {
  border-color: #28a745;
  color: #28a745;
}
.btn-outline-success:hover {
  background-color: #28a745;
  border-color: #28a745;
}
.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
}
.btn-outline-danger:hover {
  background-color: #dc3545;
  border-color: #dc3545;
}
@media (max-width: 768px) {
  .admin-parking-lots {
    padding: 1rem;
  }
  .header-actions {
    margin-top: 1rem;
  }
  .filter-tabs .nav-pills {
    flex-wrap: wrap;
  }
  .bulk-actions-panel {
    width: 95%;
    bottom: 1rem;
  }
  .bulk-actions {
    margin-top: 1rem;
  }
  .bulk-actions .btn {
    margin-bottom: 0.5rem;
    width: 100%;
  }
}
</style>