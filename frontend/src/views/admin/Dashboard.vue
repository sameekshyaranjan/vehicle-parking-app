<template>
  <div class="admin-dashboard">
    
    <div v-if="isLoading" class="loading-spinner text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading dashboard data...</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger" role="alert">
      <h4 class="alert-heading">Error Loading Dashboard</h4>
      <p>{{ error }}</p>
      <button class="btn btn-outline-danger" @click="refreshDashboard">
        <i class="fas fa-refresh me-1"></i>Retry
      </button>
    </div>
    
    <div v-else class="dashboard-content">
      
      <div class="dashboard-header mb-4">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h1 class="h3 mb-0">
              Welcome back, {{ authStore.user?.fullname || 'Admin' }}! 👋
            </h1>
            <p class="text-muted mb-0">Here's what's happening today.</p>
          </div>
          <div class="col-md-4 text-md-end">
            <button class="btn btn-outline-secondary me-2" @click="refreshDashboard">
              <i class="fas fa-sync-alt me-1"></i>Refresh
            </button>
            <span class="badge bg-success">{{ systemStatus }}</span>
          </div>
        </div>
      </div>
      
      <div class="stats-section mb-4">
        <div class="row">
          
          <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-primary">
                    <i class="fas fa-rupee-sign"></i>
                  </div>
                  <div class="ms-3">
                    <div class="stat-value">{{ todayRevenue }}</div>
                    <div class="stat-label">Today's Revenue</div>
                    <div class="stat-change" :class="revenueGrowth.color">
                      <i class="fas" :class="revenueGrowth.trend === 'up' ? 'fa-arrow-up' : 'fa-arrow-down'"></i>
                      {{ Math.abs(revenueGrowth.value) }}%
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-warning">
                    <i class="fas fa-car"></i>
                  </div>
                  <div class="ms-3">
                    <div class="stat-value">{{ activeBookings }}</div>
                    <div class="stat-label">Active Bookings</div>
                    <div class="stat-change text-info">
                      <i class="fas fa-info-circle"></i>
                      Currently active
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <div class="stat-icon" :class="`bg-${occupancyColor}`">
                    <i class="fas fa-chart-pie"></i>
                  </div>
                  <div class="ms-3">
                    <div class="stat-value">{{ occupancyRate }}</div>
                    <div class="stat-label">Occupancy Rate</div>
                    <div class="stat-change" :class="`text-${occupancyColor}`">
                      {{ dashboard.occupiedSpots }}/{{ dashboard.totalSpots }} spots
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card">
              <div class="card-body">
                <div class="d-flex align-items-center">
                  <div class="stat-icon bg-info">
                    <i class="fas fa-users"></i>
                  </div>
                  <div class="ms-3">
                    <div class="stat-value">{{ totalUsers }}</div>
                    <div class="stat-label">Total Users</div>
                    <div class="stat-change text-success">
                      <i class="fas fa-user-plus"></i>
                      Registered users
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-8">
          
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="fas fa-clock me-2"></i>Recent Activity
              </h5>
            </div>
            <div class="card-body">
              <div v-if="recentActivity.length === 0" class="text-center text-muted py-4">
                <i class="fas fa-inbox fa-3x mb-3"></i>
                <p>No recent activity</p>
              </div>
              <div v-else class="activity-list">
                <div v-for="activity in recentActivity" :key="activity.id" class="activity-item">
                  <div class="d-flex align-items-center">
                    <div class="activity-icon me-3">
                      <i class="fas" :class="getActivityIcon(activity.status)"></i>
                    </div>
                    <div class="flex-grow-1">
                      <div class="activity-title">
                        {{ activity.user_name }} parked at {{ activity.lot_name }}
                      </div>
                      <div class="activity-details text-muted">
                        Spot #{{ activity.spot_number }} • {{ activity.vehicle_number }}
                      </div>
                    </div>
                    <div class="activity-time text-muted">
                      {{ formatTimeAgo(activity.timestamp) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          
          <div class="card">
            <div class="card-header">
              <h5 class="card-title mb-0">
                <i class="fas fa-server me-2"></i>System Status
              </h5>
            </div>
            <div class="card-body">
              <div class="text-center mb-3">
                <div class="system-status-icon">
                  <i class="fas fa-check-circle text-success fa-3x"></i>
                </div>
                <h6 class="mt-2">{{ systemStatus }}</h6>
                <p class="text-muted">All systems running smoothly!</p>
              </div>
              
              <div v-if="alerts.length > 0" class="alerts-section">
                <h6 class="text-danger">
                  <i class="fas fa-exclamation-triangle me-1"></i>Alerts
                </h6>
                <div v-for="alert in alerts" :key="alert.timestamp"
                     class="alert alert-sm"
                     :class="getAlertColor(alert.type)">
                  <i class="fas" :class="getAlertIcon(alert.type)"></i>
                  {{ alert.message }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <section v-if="reservationAudit || auditError" class="card mt-4" aria-labelledby="reservation-audit-title">
        <div class="card-header">
          <h5 id="reservation-audit-title" class="card-title mb-0">Reservation Activity</h5>
        </div>
        <div class="card-body">
          <p v-if="auditError" class="text-muted mb-0" role="status">Unable to load reservation activity.</p>
          <p v-else-if="!reservationAudit.length" class="text-muted mb-0">No recorded releases yet.</p>
          <div v-else class="table-responsive">
            <table class="table align-middle mb-0">
              <thead>
                <tr>
                  <th scope="col">Reservation</th>
                  <th scope="col">Event</th>
                  <th scope="col">Recorded at</th>
                  <th scope="col" class="text-end">Final cost</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="entry in reservationAudit" :key="entry.id">
                  <td>#{{ entry.reservation_id }}</td>
                  <td>{{ entry.event_type }}</td>
                  <td>{{ formatAuditTime(entry.recorded_at) }}</td>
                  <td class="text-end">{{ entry.final_cost === null ? '—' : adminStore.formatCurrency(entry.final_cost) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>
<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'
import { useAdminStore } from '@/store/modules/admin'
import { API_BASE_URL } from '@/services/base-url'
export default {
  name: 'AdminDashboard',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const adminStore = useAdminStore()
    const refreshInterval = ref(null)
    const autoRefresh = ref(true)
    const refreshRate = ref(30000)
    const dashboard = computed(() => adminStore.dashboard)
    const isLoading = computed(() => adminStore.isLoading)
    const error = computed(() => adminStore.error)
    const reservationAudit = ref(null)
    const auditError = ref(false)
    const todayRevenue = computed(() =>
      adminStore.formatCurrency(dashboard.value.todayRevenue || 0)
    )
    const totalUsers = computed(() =>
      adminStore.formatNumber(dashboard.value.totalUsers || 0)
    )
    const occupancyRate = computed(() =>
      `${dashboard.value.occupancyRate || 0}%`
    )
    const activeBookings = computed(() =>
      adminStore.formatNumber(dashboard.value.activeBookings || 0)
    )
    const revenueGrowth = computed(() =>
      adminStore.revenueGrowthIndicator
    )
    const occupancyColor = computed(() =>
      adminStore.occupancyStatusColor
    )
    const systemStatus = computed(() =>
      adminStore.systemHealthStatus
    )
    const recentActivity = computed(() =>
      dashboard.value.recentActivity || []
    )
    const alerts = computed(() =>
      dashboard.value.alerts || []
    )
    const fetchReservationAudit = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/admin/reservation-audit`, {
          headers: { Authorization: `Bearer ${authStore.accessToken}` }
        })
        if (response.status === 404) {
          reservationAudit.value = null
        } else {
          if (!response.ok) throw new Error('Unable to load reservation activity')
          reservationAudit.value = (await response.json()).data
        }
        auditError.value = false
      } catch {
        auditError.value = true
      }
    }
    const formatAuditTime = (timestamp) => new Date(timestamp).toLocaleString()
    const refreshDashboard = async () => {
      try {
        console.log('🔄 Refreshing dashboard data...')
        await Promise.all([adminStore.fetchDashboard(), fetchReservationAudit()])
        console.log('✅ Dashboard data loaded successfully')
      } catch (error) {
        console.error('❌ Error refreshing dashboard:', error)
      }
    }
    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const time = new Date(timestamp)
      const diffMs = now - time
      const diffMins = Math.floor(diffMs / 60000)
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      const diffHours = Math.floor(diffMins / 60)
      if (diffHours < 24) return `${diffHours}h ago`
      const diffDays = Math.floor(diffHours / 24)
      return `${diffDays}d ago`
    }
    const getActivityIcon = (status) => {
      return status === 'Active' ? 'fa-car' : 'fa-check-circle'
    }
    const getAlertIcon = (type) => {
      const icons = {
        'info': 'fa-info-circle',
        'warning': 'fa-exclamation-triangle',
        'error': 'fa-times-circle',
        'success': 'fa-check-circle'
      }
      return icons[type] || 'fa-info-circle'
    }
    const getAlertColor = (type) => {
      const colors = {
        'info': 'alert-info',
        'warning': 'alert-warning',
        'error': 'alert-danger',
        'success': 'alert-success'
      }
      return colors[type] || 'alert-info'
    }
    const startAutoRefresh = () => {
      if (refreshInterval.value) {
        clearInterval(refreshInterval.value)
      }
      refreshInterval.value = setInterval(() => {
        if (!isLoading.value) {
          refreshDashboard()
        }
      }, refreshRate.value)
    }
    const stopAutoRefresh = () => {
      if (refreshInterval.value) {
        clearInterval(refreshInterval.value)
        refreshInterval.value = null
      }
    }
    onMounted(async () => {
      console.log('🚀 Dashboard component mounted')
      console.log('🔐 Auth token:', authStore.accessToken ? 'Present' : 'Missing')
      try {
        await refreshDashboard()
        if (autoRefresh.value) {
          startAutoRefresh()
        }
      } catch (error) {
        console.error('❌ Error in onMounted:', error)
      }
    })
    onUnmounted(() => {
      console.log('🛑 Dashboard component unmounted')
      stopAutoRefresh()
    })
    return {
      authStore,
      adminStore,
      dashboard,
      isLoading,
      error,
      todayRevenue,
      totalUsers,
      occupancyRate,
      activeBookings,
      revenueGrowth,
      occupancyColor,
      systemStatus,
      recentActivity,
      reservationAudit,
      auditError,
      formatAuditTime,
      alerts,
      refreshDashboard,
      formatTimeAgo,
      getActivityIcon,
      getAlertIcon,
      getAlertColor
    }
  }
}
</script>
<style scoped>
.admin-dashboard {
  padding: 1.5rem;
}
.text-muted {
  color: #00cccc !important;
}
.h3 {
  color: #00cccc !important;
}
.dashboard-header h1 {
  color: #000133;
  font-weight: 700;
}
.stat-card {
  border: none;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 1, 51, 0.1);
  transition: transform 0.2s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
}
.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;
}
.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #000133;
  line-height: 1;
}
.stat-label {
  color: #6c757d;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}
.stat-change {
  font-size: 0.8rem;
  font-weight: 600;
}
.activity-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
}
.activity-item:last-child {
  border-bottom: none;
}
.activity-icon {
  width: 36px;
  height: 36px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4B006E;
}
.activity-title {
  font-weight: 600;
  color: #000133;
}
.activity-details {
  font-size: 0.875rem;
}
.activity-time {
  font-size: 0.8rem;
}
.system-status-icon {
  margin-bottom: 1rem;
}
.loading-spinner {
  min-height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
@media (max-width: 768px) {
  .admin-dashboard {
    padding: 1rem;
  }
  .dashboard-header {
    text-align: center;
  }
  .dashboard-header .col-md-4 {
    margin-top: 1rem;
  }
}
</style>
