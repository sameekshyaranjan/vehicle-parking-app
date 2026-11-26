import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
export const useParkingStore = defineStore('parking', () => {
  const authStore = useAuthStore()
  const availableLots = ref([])
  const selectedLot = ref(null)
  const bookingHistory = ref([])
  const activeReservation = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
  const cache = ref({
    availableLots: null,
    lastFetch: null,
    cacheTimeout: 5 * 60 * 1000
  })
  const availableLotsCount = computed(() => availableLots.value.length)
  const totalAvailableSpots = computed(() =>
    availableLots.value.reduce((total, lot) => total + lot.available_spots, 0)
  )
  const hasActiveReservation = computed(() => !!activeReservation.value)
  const favoriteLocations = computed(() => {
    const locationCounts = {}
    bookingHistory.value.forEach(booking => {
      const location = booking.lot_name
      locationCounts[location] = (locationCounts[location] || 0) + 1
    })
    return Object.entries(locationCounts)
      .sort(([,a], [,b]) => b - a)
      .slice(0, 3)
      .map(([location, count]) => ({ location, count }))
  })
  const recentBookings = computed(() =>
    bookingHistory.value
      .sort((a, b) => new Date(b.parking_timestamp) - new Date(a.parking_timestamp))
      .slice(0, 5)
  )
  const fetchAvailableLots = async (forceRefresh = false) => {
    const now = Date.now()
    if (!forceRefresh &&
        cache.value.availableLots &&
        cache.value.lastFetch &&
        (now - cache.value.lastFetch) < cache.value.cacheTimeout) {
      availableLots.value = cache.value.availableLots
      return
    }
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`http://localhost:5000/api/user/parking-lots`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Failed to fetch available parking lots')
      }
      availableLots.value = data.data
      cache.value.availableLots = data.data
      cache.value.lastFetch = now
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const bookParkingSpot = async (bookingData) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`http://localhost:5000/api/user/book-parking`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(bookingData)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Failed to book parking spot')
      }
      await Promise.all([
        fetchAvailableLots(true),
        fetchActiveReservation()
      ])
      cache.value.availableLots = null
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchBookingHistory = async (page = 1, perPage = 10) => {
    isLoading.value = true
    try {
      const response = await fetch(`$'http://localhost:5000/api/user/my-bookings?page=${page}&per_page=${perPage}`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Failed to fetch booking history')
      }
      if (page === 1) {
        bookingHistory.value = data.data.bookings
      } else {
        bookingHistory.value.push(...data.data.bookings)
      }
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchActiveReservation = async () => {
    try {
      const response = await fetch( 'http://localhost:5000/api/user/active-reservation', {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        if (response.status === 404) {
          activeReservation.value = null
          return null
        }
        throw new Error(data.message || 'Failed to fetch active reservation')
      }
      activeReservation.value = data.data
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }
  const exportParkingHistory = async () => {
    isLoading.value = true
    try {
      const response = await fetch('http://localhost:5000/api/user/export-history', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.message || 'Failed to initiate export')
      }
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const selectLot = (lot) => {
    selectedLot.value = lot
  }
  const clearSelectedLot = () => {
    selectedLot.value = null
  }
  const clearError = () => {
    error.value = null
  }
  const clearCache = () => {
    cache.value.availableLots = null
    cache.value.lastFetch = null
  }
  return {
    availableLots,
    selectedLot,
    bookingHistory,
    activeReservation,
    isLoading,
    error,
    availableLotsCount,
    totalAvailableSpots,
    hasActiveReservation,
    favoriteLocations,
    recentBookings,
    fetchAvailableLots,
    bookParkingSpot,
    fetchBookingHistory,
    fetchActiveReservation,
    exportParkingHistory,
    selectLot,
    clearSelectedLot,
    clearError,
    clearCache
  }
})