import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
import { API_BASE_URL } from '@/services/base-url'
export const useUserStore = defineStore('user', () => {
  const authStore = useAuthStore()
  const userStats = ref({
    totalBookings: 0,
    bookingGrowth: 0,
    totalHours: 0,
    avgDuration: 0,
    totalSpent: 0,
    avgCost: 0,
    totalSavings: 0,
    savingsRate: 0
  })
  const activeReservation = ref(null)
  const recentBookings = ref([])
  const favoriteLocations = ref([])
  const nearbyLots = ref(0)
  const availableSpots = ref(0)
  const notifications = ref([])
  const bookingStats = ref({
    total: 0,
    completed: 0,
    active: 0,
    totalSpent: 0
  })
  const activeBooking = ref(null)
  const bookingHistory = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const quickSearch = ref({
    location: '',
    date: '',
    time: ''
  })
  const dashboard = ref({
    totalBookings: 0,
    activeBookings: 0,
    totalSpent: 0,
    recentBookings: []
  })
  const statistics = ref({
    monthlyStats: [],
    lotUsage: []
  })
  const preferences = ref({
    notifications: {
      email: true,
      sms: false,
      push: true
    },
    theme: 'auto',
    language: 'en',
    defaultLocation: null
  })
  const reportData = ref({
    totalSpending: 0,
    revenueGrowth: 0,
    totalSessions: 0,
    sessionGrowth: 0,
    avgDuration: 0,
    durationChange: 0,
    totalSavings: 0,
    satisfactionRate: 94,
    satisfactionGrowth: 2.1,
    efficiencyRate: 89,
    efficiencyGrowth: 4.5
  })
  const costBreakdown = ref([])
  const topLocations = ref([])
  const parkingInsights = ref([])
  const weeklyData = ref([])
  const monthlyData = ref([])
  const locationData = ref([])
  const selectedTimeRange = ref('30d')
  const totalBookings = computed(() => userStats.value.totalBookings)
  const hasActiveReservation = computed(() => !!activeReservation.value)
  const hasActiveBooking = computed(() => !!activeBooking.value)
  const averageSpentPerBooking = computed(() => {
    if (userStats.value.totalBookings === 0) return 0
    return userStats.value.avgCost
  })
  const monthlySpendingTrend = computed(() => {
    return statistics.value.monthlyStats.map(stat => ({
      month: stat.month,
      spending: stat.spending,
      bookings: stat.bookings
    }))
  })
  const topParkingLocations = computed(() => {
    return statistics.value.lotUsage
      .sort((a, b) => b.usage_count - a.usage_count)
      .slice(0, 5)
  })
  const unreadNotifications = computed(() =>
    notifications.value.filter(notification => !notification.read)
  )
  const spendingTrend = computed(() => {
    const change = reportData.value.revenueGrowth
    return {
      type: change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral',
      icon: change > 0 ? 'fa-arrow-up' : change < 0 ? 'fa-arrow-down' : 'fa-minus',
      percentage: Math.abs(change)
    }
  })
  const totalSavingsFormatted = computed(() => {
    return reportData.value.totalSavings.toLocaleString('en-IN')
  })
  const monthlyTrend = computed(() => {
    return monthlyData.value.map(month => ({
      month: month.month,
      sessions: month.sessions,
      spending: month.amount,
      growth: month.growth
    }))
  })
  const fetchDashboardData = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE_URL}/user/dashboard`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch dashboard data')
      }
      userStats.value = data.data.userStats
      activeReservation.value = data.data.activeReservation
      recentBookings.value = data.data.recentBookings
      favoriteLocations.value = data.data.favoriteLocations
      nearbyLots.value = data.data.nearbyLots
      availableSpots.value = data.data.availableSpots
      notifications.value = data.data.notifications
      bookingStats.value = {
        total: data.data.userStats.totalBookings,
        completed: data.data.userStats.totalBookings - (data.data.activeReservation ? 1 : 0),
        active: data.data.activeReservation ? 1 : 0,
        totalSpent: data.data.userStats.totalSpent
      }
      activeBooking.value = data.data.activeReservation
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const searchLocations = async (searchCriteria) => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/user/quick-search`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(searchCriteria)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to search locations')
      }
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const quickBookFavorite = async (location) => {
    return { locationId: location.id, locationName: location.name }
  }
  const markNotificationRead = async (notificationId) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.read = true
    }
  }
  const markAllNotificationsRead = async () => {
    notifications.value.forEach(notification => {
      notification.read = true
    })
  }
  const fetchMyBookingsData = async () => {
    return fetchDashboardData()
  }
  const fetchBookingHistory = async (page = 1, perPage = 20) => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/user/my-bookings?page=${page}&per_page=${perPage}`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch booking history')
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
  const extendBooking = async (bookingId, additionalHours) => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/user/extend-booking/${bookingId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify({ additional_hours: additionalHours })
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to extend booking')
      }
      await fetchDashboardData()
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const releaseBooking = async (bookingId, rating) => {
    isLoading.value = true;
    error.value = null;
    if (rating === undefined || rating === null) {
      const errorMessage = "Developer Error: 'releaseBooking' was called without a rating. Please provide a rating when calling this function.";
      console.error(errorMessage);
      error.value = errorMessage;
      isLoading.value = false;
      throw new Error(errorMessage);
    }
    const requestBody = { rating };
    console.log(`Attempting to release booking #${bookingId} with rating: ${rating}`);
    console.log('Request Body:', JSON.stringify(requestBody));
    try {
      const response = await fetch(`${API_BASE_URL}/user/release-parking/${bookingId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(requestBody)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to release booking');
      }
      console.log('Booking released successfully:', data);
      activeReservation.value = null;
      activeBooking.value = null;
      await fetchDashboardData();
      return data;
    } catch (err) {
      console.error('Error during releaseBooking API call:', err);
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };
  const fetchDashboard = async () => {
    return fetchDashboardData()
  }
  const fetchStatistics = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/user/statistics`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch statistics')
      }
      statistics.value = data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const updatePreferences = async (newPreferences) => {
    isLoading.value = true
    try {
      preferences.value = { ...preferences.value, ...newPreferences }
      localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
      return { success: true }
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const loadPreferences = () => {
    try {
      const stored = localStorage.getItem('userPreferences')
      if (stored) {
        preferences.value = { ...preferences.value, ...JSON.parse(stored) }
      }
    } catch (error) {
      console.error('Failed to load user preferences:', error)
    }
  }
  const clearError = () => {
    error.value = null
  }
  const fetchUserReports = async (timeRange = '30d') => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE_URL}/user/statistics/detailed?time_range=${timeRange}`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch user reports')
      }
      reportData.value = data.data.reportData
      costBreakdown.value = data.data.costBreakdown
      topLocations.value = data.data.favoriteLocations
      parkingInsights.value = data.data.parkingInsights
      weeklyData.value = data.data.weeklyData
      monthlyData.value = data.data.monthlyData
      locationData.value = data.data.locationData
      selectedTimeRange.value = timeRange
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
   const exportUserReport = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`${API_BASE_URL}/user/export-history`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to export report')
      }
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const getGrowthClass = (growth) => {
    if (growth > 0) return 'bg-success'
    if (growth < 0) return 'bg-danger'
    return 'bg-secondary'
  }
  const getProgressClass = (progress) => {
    if (progress < 70) return 'bg-success'
    if (progress < 90) return 'bg-warning'
    return 'bg-danger'
  }
  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-IN').format(num)
  }
const exportBookingHistory = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`${API_BASE_URL}/user/export-history`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to download CSV.')
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = "parking_history.csv";
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  loadPreferences()
  return {
    userStats,
    activeReservation,
    recentBookings,
    favoriteLocations,
    nearbyLots,
    availableSpots,
    notifications,
    quickSearch,
    bookingStats,
    activeBooking,
    bookingHistory,
    isLoading,
    error,
    reportData,
    costBreakdown,
    topLocations,
    parkingInsights,
    weeklyData,
    monthlyData,
    locationData,
    selectedTimeRange,
    totalBookings,
    hasActiveReservation,
    hasActiveBooking,
    averageSpentPerBooking,
    monthlySpendingTrend,
    topParkingLocations,
    unreadNotifications,
    spendingTrend,
    totalSavingsFormatted,
    monthlyTrend,
    fetchDashboardData,
    searchLocations,
    quickBookFavorite,
    markNotificationRead,
    markAllNotificationsRead,
    fetchMyBookingsData,
    fetchBookingHistory,
    extendBooking,
    releaseBooking,
    exportBookingHistory,
    fetchUserReports,
    exportUserReport,
    getGrowthClass,
    getProgressClass,
    formatNumber,
    fetchDashboard,
    fetchStatistics,
    updatePreferences,
    loadPreferences,
    clearError
  }
})