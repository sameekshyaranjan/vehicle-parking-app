<template>
  <div class="admin-charts">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary mb-1">
          <i class="fas fa-chart-bar me-2"></i>Analytics & Statistics
        </h4>
        <p class="text-muted mb-0">Comprehensive insights and performance metrics</p>
      </div>
      <div class="d-flex gap-2">
        <select v-model="timeRange" class="form-select form-select-sm" style="width: auto;">
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
          <option value="1y">Last Year</option>
        </select>
        <button class="btn btn-outline-primary btn-sm" @click="refreshData">
          <i class="fas fa-sync me-1"></i>Refresh
        </button>
        <button class="btn btn-primary btn-sm" @click="exportReport">
          <i class="fas fa-download me-1"></i>Export
        </button>
      </div>
    </div>
    
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="metric-card revenue">
          <div class="metric-icon">
            <i class="fas fa-rupee-sign"></i>
          </div>
          <div class="metric-content">
            <h6>Total Revenue</h6>
            <h3>₹{{ formatNumber(totalRevenue) }}</h3>
            <div class="metric-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ revenueGrowth }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card bookings">
          <div class="metric-icon">
            <i class="fas fa-calendar-check"></i>
          </div>
          <div class="metric-content">
            <h6>Total Bookings</h6>
            <h3>{{ formatNumber(totalBookings) }}</h3>
            <div class="metric-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ bookingsGrowth }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card occupancy">
          <div class="metric-icon">
            <i class="fas fa-percentage"></i>
          </div>
          <div class="metric-content">
            <h6>Avg Occupancy</h6>
            <h3>{{ avgOccupancy }}%</h3>
            <div class="metric-change neutral">
              <i class="fas fa-minus"></i>
              {{ occupancyChange }}%
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card efficiency">
          <div class="metric-icon">
            <i class="fas fa-chart-line"></i>
          </div>
          <div class="metric-content">
            <h6>Efficiency Rate</h6>
            <h3>{{ efficiencyRate }}%</h3>
            <div class="metric-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ efficiencyGrowth }}%
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mb-4">
      
      <div class="col-lg-8">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-chart-line me-2"></i>
              Daily Revenue Trend
            </h6>
            <div class="chart-controls">
              <div class="btn-group btn-group-sm" role="group">
                <input type="radio" class="btn-check" id="revenue-line" v-model="revenueChartType" value="line">
                <label class="btn btn-outline-primary" for="revenue-line">Line</label>
                <input type="radio" class="btn-check" id="revenue-bar" v-model="revenueChartType" value="bar">
                <label class="btn btn-outline-primary" for="revenue-bar">Bar</label>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div class="chart-placeholder" id="revenueChart">
              <canvas ref="revenueCanvas" width="600" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-doughnut-bitten me-2"></i>
              Current Occupancy
            </h6>
          </div>
          <div class="chart-body">
            <div class="occupancy-chart">
              <div class="occupancy-circle">
                <svg viewBox="0 0 100 100" class="circular-progress">
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="#e9ecef"
                    stroke-width="8"
                  />
                  <circle
                    cx="50"
                    cy="50"
                    r="45"
                    fill="none"
                    stroke="url(#gradient)"
                    stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="strokeDashoffset"
                    transform="rotate(-90 50 50)"
                  />
                  <defs>
                    <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" :style="`stop-color:${primaryColor}`" />
                      <stop offset="100%" :style="`stop-color:${secondaryColor}`" />
                    </linearGradient>
                  </defs>
                </svg>
                <div class="occupancy-text">
                  <div class="occupancy-percentage">{{ avgOccupancy }}%</div>
                  <div class="occupancy-label">Occupied</div>
                </div>
              </div>
              <div class="occupancy-stats">
                <div class="stat-row">
                  <span class="stat-label">Total Spots:</span>
                  <span class="stat-value">{{ totalSpots }}</span>
                </div>
                <div class="stat-row">
                  <span class="stat-label">Occupied:</span>
                  <span class="stat-value text-danger">{{ occupiedSpots }}</span>
                </div>
                <div class="stat-row">
                  <span class="stat-label">Available:</span>
                  <span class="stat-value text-success">{{ availableSpots }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row mb-4">
      
      <div class="col-lg-6">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-trophy me-2"></i>
              Top Performing Lots
            </h6>
          </div>
          <div class="chart-body">
            <div class="lot-rankings">
              <div
                v-for="(lot, index) in topLots"
                :key="lot.id"
                class="lot-ranking-item"
              >
                <div class="ranking-position">
                  <span class="position-number" :class="getRankingClass(index)">
                    {{ index + 1 }}
                  </span>
                </div>
                <div class="lot-info flex-grow-1">
                  <div class="lot-name">{{ lot.lot_name }}</div>
                  <div class="lot-metrics">
                    <span class="metric">{{ lot.total_reservations }} bookings</span>
                    <span class="metric">₹{{ formatNumber(lot.revenue) }} revenue</span>
                  </div>
                </div>
                <div class="lot-progress">
                  <div class="progress">
                    <div
                      class="progress-bar"
                      :style="{ width: (lot.total_reservations / topLots[0].total_reservations * 100) + '%' }"
                    ></div>
                  </div>
                  <small class="text-muted">{{ Math.round(lot.total_reservations / topLots[0].total_reservations * 100) }}%</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-6">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-users me-2"></i>
              User Activity Overview
            </h6>
          </div>
          <div class="chart-body">
            <div class="activity-overview">
              <div class="activity-metric">
                <div class="activity-icon bg-primary">
                  <i class="fas fa-user-plus"></i>
                </div>
                <div class="activity-content">
                  <h4>{{ newUsers }}</h4>
                  <p>New Users</p>
                  <small class="text-success">+{{ newUsersGrowth }}% this week</small>
                </div>
              </div>
              <div class="activity-metric">
                <div class="activity-icon bg-success">
                  <i class="fas fa-user-check"></i>
                </div>
                <div class="activity-content">
                  <h4>{{ activeUsers }}</h4>
                  <p>Active Users</p>
                  <small class="text-info">{{ Math.round(activeUsers / totalUsers * 100) }}% of total</small>
                </div>
              </div>
              <div class="activity-metric">
                <div class="activity-icon bg-warning">
                  <i class="fas fa-car"></i>
                </div>
                <div class="activity-content">
                  <h4>{{ currentlyParked }}</h4>
                  <p>Currently Parked</p>
                  <small class="text-primary">{{ Math.round(currentlyParked / totalSpots * 100) }}% capacity</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="row">
      
      <div class="col-lg-8">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-clock me-2"></i>
              Hourly Usage Pattern
            </h6>
            <div class="chart-controls">
              <select v-model="usagePatternDay" class="form-select form-select-sm">
                <option value="avg">Average Day</option>
                <option value="monday">Monday</option>
                <option value="tuesday">Tuesday</option>
                <option value="wednesday">Wednesday</option>
                <option value="thursday">Thursday</option>
                <option value="friday">Friday</option>
                <option value="saturday">Saturday</option>
                <option value="sunday">Sunday</option>
              </select>
            </div>
          </div>
          <div class="chart-body">
            <div class="usage-pattern">
              <div class="hour-bars">
                <div
                  v-for="hour in hourlyData"
                  :key="hour.hour"
                  class="hour-bar"
                  :style="{ height: (hour.usage / maxHourlyUsage * 100) + '%' }"
                  :title="`${hour.hour}:00 - ${hour.usage} bookings`"
                >
                  <div class="hour-value">{{ hour.usage }}</div>
                </div>
              </div>
              <div class="hour-labels">
                <div v-for="i in 24" :key="i" class="hour-label">
                  {{ i - 1 }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-stream me-2"></i>
              Recent Activity
            </h6>
          </div>
          <div class="chart-body">
            <div class="activity-feed">
              <div
                v-for="activity in recentActivities"
                :key="activity.id"
                class="activity-item"
              >
                <div class="activity-icon" :class="getActivityIconClass(activity.type)">
                  <i class="fas" :class="getActivityIcon(activity.type)"></i>
                </div>
                <div class="activity-content">
                  <div class="activity-text">{{ activity.description }}</div>
                  <div class="activity-time">{{ formatTimeAgo(activity.timestamp) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useAdminStore } from '../../store/modules/admin'
export default {
  name: 'AdminCharts',
  setup() {
    const adminStore = useAdminStore()
    const timeRange = ref('30d')
    const revenueChartType = ref('line')
    const usagePatternDay = ref('avg')
    const revenueCanvas = ref(null)
    const totalRevenue = ref(125000)
    const revenueGrowth = ref(12.5)
    const totalBookings = ref(2840)
    const bookingsGrowth = ref(8.3)
    const avgOccupancy = ref(75)
    const occupancyChange = ref(2.1)
    const efficiencyRate = ref(89)
    const efficiencyGrowth = ref(4.2)
    const totalSpots = ref(500)
    const occupiedSpots = ref(375)
    const availableSpots = ref(125)
    const newUsers = ref(48)
    const newUsersGrowth = ref(15)
    const activeUsers = ref(234)
    const totalUsers = ref(456)
    const currentlyParked = ref(89)
    const topLots = ref([
      { id: 1, lot_name: 'Central Mall Parking', total_reservations: 450, revenue: 22500 },
      { id: 2, lot_name: 'Airport Terminal 1', total_reservations: 320, revenue: 32000 },
      { id: 3, lot_name: 'Office Complex', total_reservations: 280, revenue: 14000 },
      { id: 4, lot_name: 'Shopping Center', total_reservations: 150, revenue: 7500 },
      { id: 5, lot_name: 'Metro Station', total_reservations: 100, revenue: 5000 }
    ])
    const hourlyData = ref(Array.from({ length: 24 }, (_, i) => ({
      hour: i,
      usage: Math.floor(Math.random() * 50) + 10
    })))
    const recentActivities = ref([
      { id: 1, type: 'booking', description: 'New booking at Central Mall', timestamp: new Date(Date.now() - 5 * 60000) },
      { id: 2, type: 'user', description: 'New user registered: John Doe', timestamp: new Date(Date.now() - 15 * 60000) },
      { id: 3, type: 'release', description: 'Spot released at Airport Terminal', timestamp: new Date(Date.now() - 30 * 60000) },
      { id: 4, type: 'booking', description: 'Booking confirmed at Office Complex', timestamp: new Date(Date.now() - 45 * 60000) },
      { id: 5, type: 'admin', description: 'New parking lot added', timestamp: new Date(Date.now() - 60 * 60000) }
    ])
    const primaryColor = computed(() => '#000133')
    const secondaryColor = computed(() => '#4B006E')
    const textAccent = computed(() => '#8AB8FE')
    const circumference = computed(() => 2 * Math.PI * 45)
    const strokeDashoffset = computed(() =>
      circumference.value - (avgOccupancy.value / 100) * circumference.value
    )
    const maxHourlyUsage = computed(() =>
      Math.max(...hourlyData.value.map(h => h.usage))
    )
    const formatNumber = (num) => {
      if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M'
      if (num >= 1000) return (num / 1000).toFixed(1) + 'K'
      return num.toString()
    }
    const getRankingClass = (index) => {
      return {
        'rank-first': index === 0,
        'rank-second': index === 1,
        'rank-third': index === 2
      }
    }
    const getActivityIconClass = (type) => {
      return {
        'activity-booking': type === 'booking',
        'activity-user': type === 'user',
        'activity-release': type === 'release',
        'activity-admin': type === 'admin'
      }
    }
    const getActivityIcon = (type) => {
      const icons = {
        booking: 'fa-plus-circle',
        user: 'fa-user-plus',
        release: 'fa-minus-circle',
        admin: 'fa-cog'
      }
      return icons[type] || 'fa-info-circle'
    }
    const formatTimeAgo = (timestamp) => {
      const now = new Date()
      const diffMs = now - new Date(timestamp)
      const diffMins = Math.floor(diffMs / 60000)
      if (diffMins < 1) return 'Just now'
      if (diffMins < 60) return `${diffMins}m ago`
      const diffHours = Math.floor(diffMins / 60)
      if (diffHours < 24) return `${diffHours}h ago`
      const diffDays = Math.floor(diffHours / 24)
      return `${diffDays}d ago`
    }
    const drawRevenueChart = () => {
      const canvas = revenueCanvas.value
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      const width = canvas.width
      const height = canvas.height
      ctx.clearRect(0, 0, width, height)
      const data = [8500, 9200, 7800, 10500, 11200, 9800, 12000]
      const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      const padding = 40
      const chartWidth = width - 2 * padding
      const chartHeight = height - 2 * padding
      const maxValue = Math.max(...data)
      const stepX = chartWidth / (data.length - 1)
      const stepY = chartHeight / maxValue
      ctx.strokeStyle = '#f0f0f0'
      ctx.lineWidth = 1
      for (let i = 0; i <= 5; i++) {
        const y = padding + (i * chartHeight / 5)
        ctx.beginPath()
        ctx.moveTo(padding, y)
        ctx.lineTo(width - padding, y)
        ctx.stroke()
      }
      ctx.strokeStyle = secondaryColor.value
      ctx.lineWidth = 3
      ctx.beginPath()
      data.forEach((value, index) => {
        const x = padding + index * stepX
        const y = height - padding - value * stepY
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      ctx.stroke()
      ctx.fillStyle = secondaryColor.value
      data.forEach((value, index) => {
        const x = padding + index * stepX
        const y = height - padding - value * stepY
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })
      ctx.fillStyle = '#666'
      ctx.font = '12px sans-serif'
      ctx.textAlign = 'center'
      labels.forEach((label, index) => {
        const x = padding + index * stepX
        ctx.fillText(label, x, height - 10)
      })
    }
    const refreshData = async () => {
      console.log('Refreshing chart data...')
      await adminStore.fetchStatistics()
      await nextTick()
      drawRevenueChart()
    }
    const exportReport = () => {
      console.log('Exporting report...')
    }
    onMounted(async () => {
      await refreshData()
      await nextTick()
      drawRevenueChart()
    })
    return {
      timeRange,
      revenueChartType,
      usagePatternDay,
      revenueCanvas,
      totalRevenue,
      revenueGrowth,
      totalBookings,
      bookingsGrowth,
      avgOccupancy,
      occupancyChange,
      efficiencyRate,
      efficiencyGrowth,
      totalSpots,
      occupiedSpots,
      availableSpots,
      newUsers,
      newUsersGrowth,
      activeUsers,
      totalUsers,
      currentlyParked,
      topLots,
      hourlyData,
      recentActivities,
      primaryColor,
      secondaryColor,
      circumference,
      strokeDashoffset,
      maxHourlyUsage,
      formatNumber,
      getRankingClass,
      getActivityIconClass,
      getActivityIcon,
      formatTimeAgo,
      refreshData,
      exportReport
    }
  }
}
</script>
<style scoped>
.admin-charts {
  padding: 1rem;
}
.text-primary {
  color: var(--primary-color) !important;
}
.btn-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
.metric-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}
.metric-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 1, 51, 0.15);
}
.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
  margin-right: 1.5rem;
}
.metric-card.revenue .metric-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}
.metric-card.bookings .metric-icon {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.metric-card.occupancy .metric-icon {
  background: linear-gradient(135deg, #fd7e14, #f8b500);
}
.metric-card.efficiency .metric-icon {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}
.metric-content h6 {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}
.metric-content h3 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.metric-change {
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}
.metric-change.positive {
  color: #28a745;
}
.metric-change.negative {
  color: #dc3545;
}
.metric-change.neutral {
  color: #6c757d;
}
.chart-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  overflow: hidden;
  margin-bottom: 1rem;
}
.chart-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  padding: 1.25rem;
  border-bottom: 1px solid rgba(138, 184, 254, 0.2);
  display: flex;
  justify-content: between;
  align-items: center;
}
.chart-header h6 {
  color: var(--primary-color);
  font-weight: 600;
  margin: 0;
}
.chart-body {
  padding: 1.5rem;
}
.chart-placeholder {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.occupancy-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.occupancy-circle {
  position: relative;
  width: 150px;
  height: 150px;
  margin-bottom: 1rem;
}
.circular-progress {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.occupancy-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.occupancy-percentage {
  font-size: 2rem;
  font-weight: 700;
  color: var(--primary-color);
}
.occupancy-label {
  font-size: 0.9rem;
  color: #6c757d;
}
.occupancy-stats {
  width: 100%;
}
.stat-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
.stat-label {
  color: #6c757d;
}
.stat-value {
  font-weight: 600;
  color: var(--primary-color);
}
.lot-rankings {
  space-y: 1rem;
}
.lot-ranking-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
  margin-bottom: 1rem;
}
.ranking-position {
  margin-right: 1rem;
}
.position-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
}
.position-number.rank-first {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: var(--primary-color);
}
.position-number.rank-second {
  background: linear-gradient(135deg, #c0c0c0, #e2e8f0);
  color: var(--primary-color);
}
.position-number.rank-third {
  background: linear-gradient(135deg, #cd7f32, #d69e2e);
  color: white;
}
.lot-info {
  flex: 1;
  margin-right: 1rem;
}
.lot-name {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.lot-metrics {
  font-size: 0.85rem;
  color: #6c757d;
}
.lot-metrics .metric {
  margin-right: 1rem;
}
.lot-progress {
  width: 100px;
  text-align: center;
}
.lot-progress .progress {
  height: 8px;
  border-radius: 4px;
  background: rgba(138, 184, 254, 0.2);
  margin-bottom: 0.25rem;
}
.lot-progress .progress-bar {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border-radius: 4px;
}
.activity-overview {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.activity-metric {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
}
.activity-icon {
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
.activity-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.activity-content h4 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
}
.activity-content p {
  color: #6c757d;
  margin-bottom: 0.25rem;
}
.usage-pattern {
  height: 250px;
  position: relative;
}
.hour-bars {
  display: flex;
  align-items: end;
  height: 200px;
  gap: 0.25rem;
  margin-bottom: 1rem;
}
.hour-bar {
  flex: 1;
  background: linear-gradient(to top, var(--secondary-color), var(--text-accent));
  border-radius: 3px 3px 0 0;
  min-height: 20px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}
.hour-bar:hover {
  transform: scaleY(1.1);
  box-shadow: 0 2px 8px rgba(75, 0, 110, 0.3);
}
.hour-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.7rem;
  color: var(--primary-color);
  font-weight: 600;
}
.hour-labels {
  display: flex;
  gap: 0.25rem;
}
.hour-label {
  flex: 1;
  text-align: center;
  font-size: 0.7rem;
  color: #6c757d;
}
.activity-feed {
  max-height: 300px;
  overflow-y: auto;
}
.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(138, 184, 254, 0.1);
}
.activity-item:last-child {
  border-bottom: none;
}
.activity-item .activity-icon {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  margin-right: 0.75rem;
  font-size: 0.9rem;
}
.activity-booking .activity-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}
.activity-user .activity-icon {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.activity-release .activity-icon {
  background: linear-gradient(135deg, #fd7e14, #f8b500);
}
.activity-admin .activity-icon {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}
.activity-content {
  flex: 1;
}
.activity-text {
  font-size: 0.9rem;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.activity-time {
  font-size: 0.8rem;
  color: #6c757d;
}
.activity-feed::-webkit-scrollbar {
  width: 4px;
}
.activity-feed::-webkit-scrollbar-track {
  background: rgba(138, 184, 254, 0.1);
}
.activity-feed::-webkit-scrollbar-thumb {
  background: rgba(138, 184, 254, 0.3);
  border-radius: 2px;
}
.activity-feed::-webkit-scrollbar-thumb:hover {
  background: rgba(138, 184, 254, 0.5);
}
@media (max-width: 768px) {
  .metric-card {
    flex-direction: column;
    text-align: center;
  }
  .metric-icon {
    margin-right: 0;
    margin-bottom: 1rem;
  }
  .chart-header {
    flex-direction: column;
    gap: 1rem;
  }
  .lot-ranking-item {
    flex-direction: column;
    text-align: center;
  }
  .lot-progress {
    width: 100%;
    margin-top: 1rem;
  }
  .hour-labels .hour-label:nth-child(odd) {
    display: none;
  }
}
</style>