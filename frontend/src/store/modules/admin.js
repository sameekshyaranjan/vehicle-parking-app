import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useAuthStore } from './auth'
export const useAdminStore = defineStore('admin', () => {
  const authStore = useAuthStore()
  const dashboard = ref({
    totalLots: 0,
    totalSpots: 0,
    occupiedSpots: 0,
    availableSpots: 0,
    totalUsers: 0,
    activeBookings: 0,
    occupancyRate: 0,
    todayRevenue: 0,
    weekRevenue: 0,
    monthRevenue: 0,
    revenueGrowth: 0,
    weeklyGrowth: 0,
    todayReservations: 0,
    totalReservations: 0,
    mostPopularLot: '',
    recentActivity: [],
    systemStatus: {},
    alerts: [],
    dailyRevenueTrend: [],
    dailyBookingsTrend: []
  })
  const parkingLots = ref([])
  const parkingSpots = ref([])
  const users = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  const availableLots = computed(() =>
    parkingLots.value.filter(lot => lot.available_spots > 0)
  )
  const totalRevenue = computed(() =>
    dashboard.value.monthRevenue
  )
  const mostPopularLot = computed(() =>
    dashboard.value.mostPopularLot
  )
  const systemHealthStatus = computed(() => {
    const status = dashboard.value.systemStatus
    const allOperational = Object.values(status).every(s => s === 'operational')
    return allOperational ? 'Excellent' : 'Attention Required'
  })
  const occupancyStatusColor = computed(() => {
    const rate = dashboard.value.occupancyRate
    if (rate < 50) return 'success'
    if (rate < 80) return 'warning'
    return 'danger'
  })
  const fetchDashboard = async () => {
    isLoading.value = true
    error.value = null
    try {
      const response = await fetch(`http://localhost:5000/api/admin/dashboard`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch dashboard data')
      }
      dashboard.value = {
        totalLots: data.data.total_parking_lots,
        totalSpots: data.data.total_parking_spots,
        occupiedSpots: data.data.occupied_spots,
        availableSpots: data.data.available_spots,
        totalUsers: data.data.total_users,
        activeBookings: data.data.active_bookings,
        occupancyRate: data.data.occupancy_rate,
        todayRevenue: data.data.today_revenue,
        weekRevenue: data.data.week_revenue,
        monthRevenue: data.data.month_revenue,
        revenueGrowth: data.data.revenue_growth,
        weeklyGrowth: data.data.weekly_growth,
        todayReservations: data.data.today_reservations,
        totalReservations: data.data.total_reservations,
        mostPopularLot: data.data.most_popular_lot,
        recentActivity: data.data.recent_activity,
        systemStatus: data.data.system_status,
        alerts: data.data.alerts,
        dailyRevenueTrend: data.data.daily_revenue_trend,
        dailyBookingsTrend: data.data.daily_bookings_trend
      }
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchParkingLots = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/parking-lots`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch parking lots')
      }
      parkingLots.value = data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const createParkingLot = async (lotData) => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/parking-lots`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(lotData)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to create parking lot')
      }
      await Promise.all([fetchParkingLots(), fetchDashboard()])
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const updateParkingLot = async (lotId, lotData) => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/parking-lots/${lotId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.accessToken}`
        },
        body: JSON.stringify(lotData)
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to update parking lot')
      }
      await Promise.all([fetchParkingLots(), fetchDashboard()])
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const deleteParkingLot = async (lotId) => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/parking-lots/${lotId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete parking lot')
      }
      await Promise.all([fetchParkingLots(), fetchDashboard()])
      return data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchParkingSpots = async (lotId) => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/parking-spots/${lotId}`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch parking spots')
      }
      parkingSpots.value = data.data.spots
      return data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchUsers = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/users`, {
        headers: {
          'Authorization': `Bearer ${authStore.accessToken}`
        }
      })
      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch users')
      }
      users.value = data.data
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }
  const fetchStatistics = async () => {
    isLoading.value = true
    try {
      const response = await fetch(`http://localhost:5000/api/admin/statistics`, {
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
  const clearError = () => {
    error.value = null
  }
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR'
    }).format(amount)
  }
  const formatNumber = (num) => {
    return new Intl.NumberFormat('en-IN').format(num)
  }
  const statistics = ref({
  overview: {
    totalRevenue: 0,
    totalBookings: 0,
    activeUsers: 0,
    avgOccupancy: 0,
    satisfaction: 0,
    efficiency: 0,
    revenueGrowth: 0
  },
  geographicData: [],
  trendData: [],
  topLocations: [],
  performanceMetrics: {
    peakHours: [],
    avgSessionDuration: 0,
    locationUtilization: [],
    systemEfficiency: 0,
    customerSatisfaction: 0
  },
  timeRange: '30d'
})
const totalRevenueFormatted = computed(() =>
  formatCurrency(statistics.value.overview.totalRevenue)
)
const revenueGrowthIndicator = computed(() => {
  const growth = statistics.value.overview.revenueGrowth
  return {
    value: Math.abs(growth),
    trend: growth > 0 ? 'up' : growth < 0 ? 'down' : 'stable',
    color: growth > 0 ? 'success' : growth < 0 ? 'danger' : 'warning'
  }
})
const topPerformingAreas = computed(() =>
  statistics.value.geographicData
    .sort((a, b) => b.revenue - a.revenue)
    .slice(0, 5)
)
const fetchStatisticsOverview = async (timeRange = '30d') => {
  isLoading.value = true
  error.value = null
  try {
    const response = await fetch(`http://localhost:5000/api/admin/statistics/comprehensive?time_range=${timeRange}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch statistics overview')
    }
    statistics.value.overview = data.data.overview
    statistics.value.geographicData = data.data.geographicData
    statistics.value.trendData = data.data.trendData
    statistics.value.topLocations = data.data.topLocations
    statistics.value.timeRange = timeRange
    return data.data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    isLoading.value = false
  }
}
const fetchRevenueTrends = async (period = 'daily', days = 30) => {
  isLoading.value = true
  try {
    const response = await fetch(`http://localhost:5000/api/admin/statistics/revenue-trends?period=${period}&days=${days}`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch revenue trends')
    }
    statistics.value.trendData = data.data.trends
    return data.data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    isLoading.value = false
  }
}
const fetchPerformanceMetrics = async () => {
  isLoading.value = true
  try {
    const response = await fetch(`http://localhost:5000/api/admin/statistics/performance-metrics`, {
      headers: {
        'Authorization': `Bearer ${authStore.accessToken}`
      }
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch performance metrics')
    }
    statistics.value.performanceMetrics = data.data
    return data.data
  } catch (err) {
    error.value = err.message
    throw err
  } finally {
    isLoading.value = false
  }
}
const refreshAllStatistics = async (timeRange = '30d') => {
  try {
    await Promise.all([
      fetchStatisticsOverview(timeRange),
      fetchPerformanceMetrics()
    ])
  } catch (error) {
    console.error('Error refreshing statistics:', error)
    throw error
  }
}
  return {
    dashboard,
    parkingLots,
    parkingSpots,
    users,
    statistics,
    isLoading,
    error,
    availableLots,
    totalRevenue,
    mostPopularLot,
    systemHealthStatus,
    revenueGrowthIndicator,
    occupancyStatusColor,
    totalRevenueFormatted,
    topPerformingAreas,
    fetchDashboard,
    fetchParkingLots,
    createParkingLot,
    updateParkingLot,
    deleteParkingLot,
    fetchParkingSpots,
    fetchUsers,
    fetchStatistics,
    clearError,
    fetchStatisticsOverview,
  fetchRevenueTrends,
  fetchPerformanceMetrics,
  refreshAllStatistics,
    formatCurrency,
    formatNumber
  }
})