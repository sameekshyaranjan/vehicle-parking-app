<template>
  <div class="booking-history">
    <div class="card mb-4 filter-card">
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-md-4">
            <div class="search-box">
              <i class="fas fa-search search-icon"></i>
              <input
                v-model="searchQuery"
                type="text"
                class="form-control"
                placeholder="Search by location or vehicle..."
                @input="debouncedSearch"
              >
            </div>
          </div>
          <div class="col-md-2">
            <select v-model="statusFilter" class="form-select" @change="applyFilters">
              <option value="">All Status</option>
              <option value="Active">Active</option>
              <option value="Completed">Completed</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="sortBy" class="form-select" @change="applyFilters">
              <option value="parking_timestamp">Latest First</option>
              <option value="lot_name">Location</option>
              <option value="parking_cost">Cost: High to Low</option>
            </select>
          </div>
          <div class="col-md-3">
            <div class="view-toggle">
              <div class="btn-group w-100" role="group">
                <input
                  type="radio"
                  class="btn-check"
                  id="cardView"
                  :checked="viewMode === 'cards'"
                  @change="viewMode = 'cards'"
                >
                <label class="btn btn-outline-primary" for="cardView">
                  <i class="fas fa-th-large me-1"></i> Cards
                </label>
                <input
                  type="radio"
                  class="btn-check"
                  id="tableView"
                  :checked="viewMode === 'table'"
                  @change="viewMode = 'table'"
                >
                <label class="btn btn-outline-primary" for="tableView">
                  <i class="fas fa-table me-1"></i> Table
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="isLoading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">Loading booking history...</p>
    </div>
    <div v-else-if="paginatedBookings.length === 0" class="empty-state">
      <i class="fas fa-history fa-3x text-muted mb-3"></i>
      <h5>No Booking History Found</h5>
      <p class="text-muted">Try adjusting your search criteria.</p>
    </div>
    <div v-else-if="viewMode === 'cards'" class="cards-view">
      <div class="row">
        <div v-for="booking in paginatedBookings" :key="booking.id" class="col-lg-6 col-xl-4 mb-4">
          <div class="card booking-card" :class="getBookingCardClass(booking)">
            <div class="card-header">
              <div class="d-flex justify-content-between align-items-start">
                <div class="booking-info">
                  <h6 class="location-name">{{ booking.lot_name }}</h6>
                  <p class="booking-date">{{ formatDateTime(booking.parking_timestamp) }}</p>
                </div>
                <span class="status-badge" :class="getStatusClass(booking.status)">
                  <i class="fas me-1" :class="getStatusIcon(booking.status)"></i>
                  {{ booking.status }}
                </span>
              </div>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-6">
                  <small class="text-muted d-block">Spot</small>
                  <div class="fw-bold">#{{ booking.spot_number }}</div>
                </div>
                <div class="col-6">
                  <small class="text-muted d-block">Vehicle</small>
                  <div class="fw-bold">{{ booking.vehicle_number }}</div>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-6">
                  <small class="text-muted d-block">Duration</small>
                  <div class="fw-bold">{{ booking.duration_hours }}h</div>
                </div>
                <div class="col-6">
                  <small class="text-muted d-block">Cost</small>
                  <div class="fw-bold text-cost">₹{{ booking.parking_cost || 'N/A' }}</div>
                </div>
              </div>
            </div>
            <div class="card-footer">
              <button class="btn btn-sm btn-outline-primary w-50" @click="viewBookingDetails(booking)">
                  <i class="fas fa-eye me-1"></i>View Details
              </button>
              <button v-if="booking.status === 'Active'" class="btn btn-sm btn-success ms-2 w-50" @click="releaseBooking(booking)">
                <i class="fas fa-sign-out-alt me-1"></i>Release
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="table-view">
      <div class="table-responsive">
        <table class="table table-hover align-middle">
          <thead>
            <tr>
              <th>Date & Time</th>
              <th>Location</th>
              <th>Vehicle/Spot</th>
              <th>Duration (hrs)</th>
              <th>Cost (₹)</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="booking in paginatedBookings" :key="booking.id">
              <td>{{ formatDateTime(booking.parking_timestamp) }}</td>
              <td>{{ booking.lot_name }}</td>
              <td>
                <div class="fw-bold">{{ booking.vehicle_number }}</div>
                <small class="text-muted">Spot #{{ booking.spot_number }}</small>
              </td>
              <td>{{ booking.duration_hours }}</td>
              <td>{{ booking.parking_cost || 'N/A' }}</td>
              <td>
                <span class="status-badge" :class="getStatusClass(booking.status)">
                  {{ booking.status }}
                </span>
              </td>
              <td>
                <button class="btn btn-sm btn-outline-primary" @click="viewBookingDetails(booking)">
                  Details
                </button>
                 <button v-if="booking.status === 'Active'" class="btn btn-sm btn-success ms-2" @click="releaseBooking(booking)">
                  Release
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="totalPages > 1" class="d-flex justify-content-center mt-4">
      <nav>
        <ul class="pagination">
          <li class="page-item" :class="{ disabled: currentPage === 1 }">
            <a class="page-link" href="#" @click.prevent="currentPage--">&laquo;</a>
          </li>
          <li v-for="page in totalPages" :key="page" class="page-item" :class="{ active: page === currentPage }">
            <a class="page-link" href="#" @click.prevent="currentPage = page">{{ page }}</a>
          </li>
          <li class="page-item" :class="{ disabled: currentPage === totalPages }">
            <a class="page-link" href="#" @click.prevent="currentPage++">&raquo;</a>
          </li>
        </ul>
      </nav>
    </div>
    <div v-if="showReleaseModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-sign-out-alt me-2"></i>Confirm Release
            </h5>
            <button type="button" class="btn-close" @click="showReleaseModal = false"></button>
          </div>
          <div class="modal-body">
            <p>Please rate your experience for this parking session before releasing the spot.</p>
            <div class="rating-section text-center mt-3">
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
              <i class="fas fa-check me-1"></i>Confirm
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showDetailsModal" class="modal d-block" style="background-color: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-receipt me-2"></i>Booking Details
            </h5>
            <button type="button" class="btn-close" @click="closeDetailsModal"></button>
          </div>
          <div class="modal-body" v-if="selectedBooking">
            <div class="booking-details-grid">
              <div class="detail-item">
                <label>Location</label>
                <div>{{ selectedBooking.lot_name }}</div>
              </div>
              <div class="detail-item">
                <label>Address</label>
                <div>{{ selectedBooking.lot_address }}</div>
              </div>
              <div class="detail-item">
                <label>Spot Number</label>
                <div>#{{ selectedBooking.spot_number }}</div>
              </div>
              <div class="detail-item">
                <label>Vehicle Number</label>
                <div>{{ selectedBooking.vehicle_number }}</div>
              </div>
              <div class="detail-item">
                <label>Parking Time</label>
                <div>{{ formatDateTime(selectedBooking.parking_timestamp) }}</div>
              </div>
              <div class="detail-item">
                <label>Leaving Time</label>
                <div>{{ formatDateTime(selectedBooking.leaving_timestamp) || 'Currently Parked' }}</div>
              </div>
              <div class="detail-item">
                <label>Duration</label>
                <div>{{ selectedBooking.duration_hours }} hours</div>
              </div>
              <div class="detail-item">
                <label>Final Cost</label>
                <div class="fw-bold">₹{{ selectedBooking.parking_cost || 'N/A' }}</div>
              </div>
              <div class="detail-item full-width">
                <label>Status</label>
                <span class="status-badge" :class="getStatusClass(selectedBooking.status)">
                  {{ selectedBooking.status }}
                </span>
              </div>
              <div class="detail-item full-width" v-if="selectedBooking.remarks">
                <label>Remarks</label>
                <div>{{ selectedBooking.remarks }}</div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeDetailsModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../store/modules/user'
export default {
  name: 'BookingHistory',
  setup(_, { emit }) {
    const userStore = useUserStore()
    const searchQuery = ref('')
    const statusFilter = ref('')
    const sortBy = ref('parking_timestamp')
    const viewMode = ref('cards')
    const currentPage = ref(1)
    const itemsPerPage = ref(9)
    const showReleaseModal = ref(false)
    const releasingBooking = ref(null)
    const releaseRating = ref(5)
    const showDetailsModal = ref(false)
    const selectedBooking = ref(null)
    const isLoading = computed(() => userStore.isLoading)
    const error = computed(() => userStore.error)
    const filteredBookings = computed(() => {
      let bookings = [...userStore.bookingHistory]
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        bookings = bookings.filter(b =>
          b.lot_name.toLowerCase().includes(query) ||
          b.vehicle_number.toLowerCase().includes(query)
        )
      }
      if (statusFilter.value) {
        bookings = bookings.filter(b => b.status === statusFilter.value)
      }
      bookings.sort((a, b) => {
        if (sortBy.value === 'parking_timestamp') {
          return new Date(b.parking_timestamp) - new Date(a.parking_timestamp)
        }
        if (sortBy.value === 'lot_name') {
          return a.lot_name.localeCompare(b.lot_name)
        }
        return 0
      })
      return bookings
    })
    const totalPages = computed(() =>
      Math.ceil(filteredBookings.value.length / itemsPerPage.value)
    )
    const paginatedBookings = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage.value
      return filteredBookings.value.slice(start, start + itemsPerPage.value)
    })
    const debouncedSearch = () => {
      setTimeout(() => {
        currentPage.value = 1
      }, 300)
    }
    const applyFilters = () => {
      currentPage.value = 1
    }
    const getBookingCardClass = (booking) => {
      return {
        'border-success': booking.status === 'Active',
        'border-secondary': booking.status === 'Completed',
      }
    }
    const getStatusClass = (status) => {
      const classes = {
        'Active': 'bg-success',
        'Completed': 'bg-secondary'
      }
      return classes[status] || 'bg-secondary'
    }
    const getStatusIcon = (status) => {
      const icons = {
        'Active': 'fa-car',
        'Completed': 'fa-check-circle'
      }
      return icons[status] || 'fa-check-circle'
    }
    const formatDateTime = (dateString) => {
      if (!dateString) return null;
      return new Date(dateString).toLocaleString('en-IN', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    const viewBookingDetails = (booking) => {
      selectedBooking.value = booking
      showDetailsModal.value = true
    }
    const closeDetailsModal = () => {
      showDetailsModal.value = false
      selectedBooking.value = null
    }
    const releaseBooking = (booking) => {
      releasingBooking.value = booking
      releaseRating.value = 5
      showReleaseModal.value = true
    }
    const confirmRelease = async () => {
      if (!releasingBooking.value) return
      try {
        await userStore.releaseBooking(releasingBooking.value.id, releaseRating.value)
        await userStore.fetchBookingHistory()
      } catch (err) {
        console.error("Failed to release booking:", err)
      } finally {
        showReleaseModal.value = false
        releasingBooking.value = null
      }
    }
    onMounted(() => {
      userStore.fetchBookingHistory()
    })
    return {
      isLoading,
      error,
      searchQuery,
      statusFilter,
      sortBy,
      viewMode,
      currentPage,
      itemsPerPage,
      paginatedBookings,
      totalPages,
      debouncedSearch,
      applyFilters,
      getBookingCardClass,
      getStatusClass,
      getStatusIcon,
      formatDateTime,
      viewBookingDetails,
      closeDetailsModal,
      releaseBooking,
      showReleaseModal,
      releasingBooking,
      releaseRating,
      confirmRelease,
      showDetailsModal,
      selectedBooking,
    }
  }
}
</script>
<style scoped>
.booking-history .card {
    background: white;
    color: #333; 
}
.booking-history .filter-card {
    background-color: #f8f9fa;
}
.booking-card {
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
    border-left-width: 4px;
    border-left-style: solid;
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.booking-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 1, 51, 0.15);
}
.booking-card .card-header {
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
}
.booking-card .card-body {
    flex-grow: 1;
}
.booking-card .card-footer {
    background: #f8f9fa;
    border-top: 1px solid #dee2e6;
}
.location-name {
    color: var(--primary-color);
    font-weight: 700;
}
.booking-date {
    font-size: 0.85rem;
    color: #6c757d;
}
.text-cost {
    color: var(--secondary-color);
    font-weight: 700;
}
.status-badge {
    padding: 0.3rem 0.8rem;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    color: white;
}
.pagination .page-link {
    color: var(--secondary-color);
}
.pagination .page-item.active .page-link {
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}
.rating-section .star-rating {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}
.star-btn {
  background: none;
  border: none;
  color: #ddd;
  font-size: 2rem;
  cursor: pointer;
  transition: all 0.2s ease;
}
.star-btn:hover,
.star-btn.active {
  color: #ffc107;
  transform: scale(1.1);
}
.booking-details-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}
.detail-item {
    background-color: #f8f9fa;
    padding: 0.75rem;
    border-radius: 8px;
}
.detail-item label {
    display: block;
    font-size: 0.8rem;
    color: #6c757d;
    font-weight: 600;
    margin-bottom: 0.25rem;
}
.detail-item div {
    font-size: 1rem;
    color: #212529;
}
.detail-item.full-width {
    grid-column: span 2;
}
</style>