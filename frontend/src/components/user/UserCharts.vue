<template>
  <div class="user-charts">
    
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h4 class="text-primary mb-1">
          <i class="fas fa-chart-line me-2"></i>My Parking Analytics
        </h4>
        <p class="text-muted mb-0">Track your parking patterns and savings</p>
      </div>
      <div class="d-flex gap-2">
        <select v-model="timeRange" class="form-select form-select-sm" style="width: auto;">
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
          <option value="6m">Last 6 Months</option>
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
        <div class="metric-card total-bookings">
          <div class="metric-icon">
            <i class="fas fa-calendar-check"></i>
          </div>
          <div class="metric-content">
            <h6>Total Bookings</h6>
            <h3>{{ totalBookings }}</h3>
            <div class="metric-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ bookingsGrowth }}% vs last period
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card total-hours">
          <div class="metric-icon">
            <i class="fas fa-clock"></i>
          </div>
          <div class="metric-content">
            <h6>Total Hours</h6>
            <h3>{{ totalHours }}h</h3>
            <div class="metric-change positive">
              <i class="fas fa-arrow-up"></i>
              +{{ hoursGrowth }}% vs last period
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card total-spent">
          <div class="metric-icon">
            <i class="fas fa-rupee-sign"></i>
          </div>
          <div class="metric-content">
            <h6>Total Spent</h6>
            <h3>₹{{ totalSpent }}</h3>
            <div class="metric-change neutral">
              <i class="fas fa-minus"></i>
              {{ spentGrowth }}% vs last period
            </div>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="metric-card avg-cost">
          <div class="metric-icon">
            <i class="fas fa-calculator"></i>
          </div>
          <div class="metric-content">
            <h6>Avg Cost/Hour</h6>
            <h3>₹{{ avgCostPerHour }}</h3>
            <div class="metric-change negative">
              <i class="fas fa-arrow-down"></i>
              -{{ costReduction }}% (savings!)
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
              Spending Trend Over Time
            </h6>
            <div class="chart-controls">
              <div class="btn-group btn-group-sm" role="group">
                <input type="radio" class="btn-check" id="spending-daily" v-model="spendingViewType" value="daily">
                <label class="btn btn-outline-primary" for="spending-daily">Daily</label>
                <input type="radio" class="btn-check" id="spending-weekly" v-model="spendingViewType" value="weekly">
                <label class="btn btn-outline-primary" for="spending-weekly">Weekly</label>
                <input type="radio" class="btn-check" id="spending-monthly" v-model="spendingViewType" value="monthly">
                <label class="btn btn-outline-primary" for="spending-monthly">Monthly</label>
              </div>
            </div>
          </div>
          <div class="chart-body">
            <div class="chart-container">
              <canvas ref="spendingCanvas" width="600" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-chart-pie me-2"></i>
              Favorite Locations
            </h6>
          </div>
          <div class="chart-body">
            <div class="favorite-locations">
              <div
                v-for="(location, index) in favoriteLocations"
                :key="location.id"
                class="location-item"
              >
                <div class="location-rank">
                  <span class="rank-number" :class="getRankClass(index)">
                    {{ index + 1 }}
                  </span>
                </div>
                <div class="location-info flex-grow-1">
                  <div class="location-name">{{ location.name }}</div>
                  <div class="location-stats">
                    <span class="visits">{{ location.visits }} visits</span>
                    <span class="percentage">{{ location.percentage }}%</span>
                  </div>
                </div>
                <div class="location-visual">
                  <div class="usage-bar">
                    <div
                      class="usage-fill"
                      :style="{ width: location.percentage + '%' }"
                    ></div>
                  </div>
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
              <i class="fas fa-calendar-week me-2"></i>
              Weekly Usage Pattern
            </h6>
          </div>
          <div class="chart-body">
            <div class="weekly-pattern">
              <div
                v-for="day in weeklyData"
                :key="day.day"
                class="day-column"
              >
                <div class="day-bar-container">
                  <div
                    class="day-bar"
                    :style="{ height: (day.usage / maxWeeklyUsage * 100) + '%' }"
                    :title="`${day.day}: ${day.usage} bookings`"
                  >
                    <span class="usage-count">{{ day.usage }}</span>
                  </div>
                </div>
                <div class="day-label">{{ day.day }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="col-lg-6">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-piggy-bank me-2"></i>
              Savings Tracker
            </h6>
          </div>
          <div class="chart-body">
            <div class="savings-overview">
              <div class="savings-circle">
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
                    stroke="url(#savingsGradient)"
                    stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="circumference"
                    :stroke-dashoffset="savingsStrokeDashoffset"
                    transform="rotate(-90 50 50)"
                  />
                  <defs>
                    <linearGradient id="savingsGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" :style="`stop-color:${primaryColor}`" />
                      <stop offset="100%" :style="`stop-color:#28a745`" />
                    </linearGradient>
                  </defs>
                </svg>
                <div class="savings-text">
                  <div class="savings-amount">₹{{ totalSavings }}</div>
                  <div class="savings-label">Total Saved</div>
                </div>
              </div>
              <div class="savings-breakdown">
                <div class="savings-item">
                  <div class="savings-type">
                    <i class="fas fa-clock text-success"></i>
                    <span>Early Bird Discounts</span>
                  </div>
                  <div class="savings-value">₹{{ earlyBirdSavings }}</div>
                </div>
                <div class="savings-item">
                  <div class="savings-type">
                    <i class="fas fa-star text-warning"></i>
                    <span>Loyalty Rewards</span>
                  </div>
                  <div class="savings-value">₹{{ loyaltySavings }}</div>
                </div>
                <div class="savings-item">
                  <div class="savings-type">
                    <i class="fas fa-percentage text-info"></i>
                    <span>Special Offers</span>
                  </div>
                  <div class="savings-value">₹{{ specialOfferSavings }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
      <div class="col-lg-8">
        <div class="chart-card">
          <div class="chart-header">
            <h6>
              <i class="fas fa-hourglass-half me-2"></i>
              Parking Duration Analysis
            </h6>
          </div>
          <div class="chart-body">
            <div class="duration-analysis">
              <div class="duration-stats">
                <div class="stat-item">
                  <div class="stat-icon bg-primary">
                    <i class="fas fa-clock"></i>
                  </div>
                  <div class="stat-content">
                    <h5>{{ avgDuration }}h</h5>
                    <small>Average Duration</small>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon bg-success">
                    <i class="fas fa-thumbs-up"></i>
                  </div>
                  <div class="stat-content">
                    <h5>{{ efficiency }}%</h5>
                    <small>Parking Efficiency</small>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon bg-warning">
                    <i class="fas fa-history"></i>
                  </div>
                  <div class="stat-content">
                    <h5>{{ longestSession }}h</h5>
                    <small>Longest Session</small>
                  </div>
                </div>
              </div>
              <div class="duration-distribution">
                <h6 class="text-primary mb-3">Duration Distribution</h6>
                <div
                  v-for="range in durationRanges"
                  :key="range.label"
                  class="duration-range"
                >
                  <div class="range-label">{{ range.label }}</div>
                  <div class="range-bar">
                    <div
                      class="range-fill"
                      :style="{ width: range.percentage + '%' }"
                    ></div>
                  </div>
                  <div class="range-count">{{ range.count }}</div>
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
              <i class="fas fa-lightbulb me-2"></i>
              Smart Insights
            </h6>
          </div>
          <div class="chart-body">
            <div class="insights-list">
              <div
                v-for="insight in smartInsights"
                :key="insight.id"
                class="insight-item"
                :class="insight.type"
              >
                <div class="insight-icon">
                  <i class="fas" :class="insight.icon"></i>
                </div>
                <div class="insight-content">
                  <div class="insight-title">{{ insight.title }}</div>
                  <div class="insight-description">{{ insight.description }}</div>
                </div>
              </div>
            </div>
            <div class="achievement-badge">
              <div class="badge-icon">
                <i class="fas fa-trophy"></i>
              </div>
              <div class="badge-content">
                <h6>Smart Parker!</h6>
                <p>You've saved {{ savingsPercentage }}% compared to average users this month!</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useUserStore } from '../../store/modules/user'
export default {
  name: 'UserCharts',
  setup() {
    const userStore = useUserStore()
    const timeRange = ref('30d')
    const spendingViewType = ref('weekly')
    const spendingCanvas = ref(null)
    const totalBookings = ref(28)
    const bookingsGrowth = ref(15.2)
    const totalHours = ref(84)
    const hoursGrowth = ref(12.8)
    const totalSpent = ref(3200)
    const spentGrowth = ref(-8.5)
    const avgCostPerHour = ref(38)
    const costReduction = ref(12.3)
    const totalSavings = ref(850)
    const earlyBirdSavings = ref(420)
    const loyaltySavings = ref(280)
    const specialOfferSavings = ref(150)
    const avgDuration = ref(3.2)
    const efficiency = ref(87)
    const longestSession = ref(8.5)
    const favoriteLocations = ref([
      { id: 1, name: 'Central Mall', visits: 12, percentage: 42 },
      { id: 2, name: 'Office Complex', visits: 8, percentage: 29 },
      { id: 3, name: 'Metro Station', visits: 5, percentage: 18 },
      { id: 4, name: 'Airport Terminal', visits: 3, percentage: 11 }
    ])
    const weeklyData = ref([
      { day: 'Mon', usage: 6 },
      { day: 'Tue', usage: 8 },
      { day: 'Wed', usage: 4 },
      { day: 'Thu', usage: 7 },
      { day: 'Fri', usage: 9 },
      { day: 'Sat', usage: 3 },
      { day: 'Sun', usage: 2 }
    ])
    const durationRanges = ref([
      { label: '< 1 hour', count: 3, percentage: 12 },
      { label: '1-2 hours', count: 8, percentage: 32 },
      { label: '2-4 hours', count: 12, percentage: 48 },
      { label: '4-8 hours', count: 4, percentage: 16 },
      { label: '> 8 hours', count: 1, percentage: 4 }
    ])
    const smartInsights = ref([
      {
        id: 1,
        type: 'positive',
        icon: 'fa-thumbs-up',
        title: 'Great Timing!',
        description: 'You book during off-peak hours, saving 15% on average.'
      },
      {
        id: 2,
        type: 'info',
        icon: 'fa-map-marker-alt',
        title: 'Location Pattern',
        description: 'Central Mall is your go-to spot. Consider trying nearby alternatives.'
      },
      {
        id: 3,
        type: 'warning',
        icon: 'fa-clock',
        title: 'Duration Optimization',
        description: 'You often exceed expected duration. Try booking longer slots.'
      },
      {
        id: 4,
        type: 'success',
        icon: 'fa-piggy-bank',
        title: 'Savings Goal',
        description: 'You\'re on track to save ₹2000 this month!'
      }
    ])
    const primaryColor = computed(() => '#000133')
    const secondaryColor = computed(() => '#4B006E')
    const textAccent = computed(() => '#8AB8FE')
    const maxWeeklyUsage = computed(() =>
      Math.max(...weeklyData.value.map(d => d.usage))
    )
    const circumference = computed(() => 2 * Math.PI * 45)
    const savingsStrokeDashoffset = computed(() => {
      const percentage = Math.min(totalSavings.value / 1000 * 100, 100)
      return circumference.value - (percentage / 100) * circumference.value
    })
    const savingsPercentage = computed(() =>
      Math.round((totalSavings.value / (totalSpent.value + totalSavings.value)) * 100)
    )
    const getRankClass = (index) => {
      return {
        'rank-first': index === 0,
        'rank-second': index === 1,
        'rank-third': index === 2
      }
    }
    const drawSpendingChart = () => {
      const canvas = spendingCanvas.value
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      const width = canvas.width
      const height = canvas.height
      ctx.clearRect(0, 0, width, height)
      let data, labels
      if (spendingViewType.value === 'daily') {
        data = [120, 80, 150, 200, 180, 90, 160]
        labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
      } else if (spendingViewType.value === 'weekly') {
        data = [850, 920, 760, 1100, 980]
        labels = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
      } else {
        data = [3200, 2800, 3500, 3100, 2900, 3300]
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
      }
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
      ctx.fillStyle = `${secondaryColor.value}20`
      ctx.beginPath()
      ctx.moveTo(padding, height - padding)
      data.forEach((value, index) => {
        const x = padding + index * stepX
        const y = height - padding - value * stepY
        ctx.lineTo(x, y)
      })
      ctx.lineTo(width - padding, height - padding)
      ctx.closePath()
      ctx.fill()
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
      console.log('Refreshing user analytics...')
      await userStore.fetchStatistics()
      await nextTick()
      drawSpendingChart()
    }
    const exportReport = () => {
      console.log('Exporting user analytics report...')
    }
    onMounted(async () => {
      await refreshData()
      await nextTick()
      drawSpendingChart()
    })
    return {
      timeRange,
      spendingViewType,
      spendingCanvas,
      totalBookings,
      bookingsGrowth,
      totalHours,
      hoursGrowth,
      totalSpent,
      spentGrowth,
      avgCostPerHour,
      costReduction,
      totalSavings,
      earlyBirdSavings,
      loyaltySavings,
      specialOfferSavings,
      avgDuration,
      efficiency,
      longestSession,
      favoriteLocations,
      weeklyData,
      durationRanges,
      smartInsights,
      primaryColor,
      secondaryColor,
      textAccent,
      maxWeeklyUsage,
      circumference,
      savingsStrokeDashoffset,
      savingsPercentage,
      getRankClass,
      refreshData,
      exportReport
    }
  }
}
</script>
<style scoped>
.user-charts {
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
.btn-check:checked + .btn-outline-primary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
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
.metric-card.total-bookings .metric-icon {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.metric-card.total-hours .metric-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}
.metric-card.total-spent .metric-icon {
  background: linear-gradient(135deg, #fd7e14, #f8b500);
}
.metric-card.avg-cost .metric-icon {
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
  justify-content: space-between;
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
.chart-container {
  width: 100%;
  height: 300px;
  position: relative;
}
.favorite-locations {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.location-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
}
.location-rank {
  margin-right: 1rem;
}
.rank-number {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: white;
  font-size: 0.9rem;
}
.rank-number.rank-first {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: var(--primary-color);
}
.rank-number.rank-second {
  background: linear-gradient(135deg, #c0c0c0, #e2e8f0);
  color: var(--primary-color);
}
.rank-number.rank-third {
  background: linear-gradient(135deg, #cd7f32, #d69e2e);
  color: white;
}
.rank-number:not(.rank-first):not(.rank-second):not(.rank-third) {
  background: var(--secondary-color);
}
.location-info {
  flex: 1;
  margin-right: 1rem;
}
.location-name {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.location-stats {
  font-size: 0.85rem;
  color: #6c757d;
}
.location-stats .visits {
  margin-right: 1rem;
}
.location-stats .percentage {
  color: var(--secondary-color);
  font-weight: 600;
}
.location-visual {
  width: 60px;
}
.usage-bar {
  height: 8px;
  background: rgba(138, 184, 254, 0.2);
  border-radius: 4px;
  overflow: hidden;
}
.usage-fill {
  height: 100%;
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  border-radius: 4px;
}
.weekly-pattern {
  display: flex;
  align-items: end;
  justify-content: space-between;
  height: 200px;
  gap: 0.5rem;
}
.day-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.day-bar-container {
  flex: 1;
  display: flex;
  align-items: end;
  width: 100%;
}
.day-bar {
  width: 100%;
  background: linear-gradient(to top, var(--secondary-color), var(--text-accent));
  border-radius: 4px 4px 0 0;
  min-height: 20px;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: start;
  justify-content: center;
  padding-top: 8px;
}
.day-bar:hover {
  transform: scaleY(1.05);
  box-shadow: 0 2px 8px rgba(75, 0, 110, 0.3);
}
.usage-count {
  color: white;
  font-size: 0.8rem;
  font-weight: 600;
}
.day-label {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.5rem;
  font-weight: 600;
}
.savings-overview {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.savings-circle {
  position: relative;
  width: 120px;
  height: 120px;
  margin-bottom: 1.5rem;
}
.circular-progress {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}
.savings-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.savings-amount {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary-color);
}
.savings-label {
  font-size: 0.8rem;
  color: #6c757d;
}
.savings-breakdown {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.savings-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 8px;
}
.savings-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--primary-color);
  font-weight: 500;
}
.savings-value {
  color: var(--secondary-color);
  font-weight: 700;
}
.duration-analysis {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.duration-stats {
  display: flex;
  justify-content: space-around;
  gap: 1rem;
}
.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
  flex: 1;
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
}
.stat-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.stat-content h5 {
  color: var(--primary-color);
  font-weight: 700;
  margin: 0;
}
.stat-content small {
  color: #6c757d;
}
.duration-distribution {
  flex: 1;
}
.duration-range {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.range-label {
  width: 80px;
  font-size: 0.9rem;
  color: #6c757d;
}
.range-bar {
  flex: 1;
  height: 20px;
  background: rgba(138, 184, 254, 0.2);
  border-radius: 10px;
  overflow: hidden;
}
.range-fill {
  height: 100%;
  background: linear-gradient(135deg, var(--secondary-color), var(--text-accent));
  border-radius: 10px;
}
.range-count {
  width: 30px;
  text-align: right;
  font-weight: 600;
  color: var(--primary-color);
}
.insights-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}
.insight-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  border-radius: 10px;
  border-left: 4px solid;
}
.insight-item.positive {
  background: rgba(40, 167, 69, 0.1);
  border-left-color: #28a745;
}
.insight-item.info {
  background: rgba(23, 162, 184, 0.1);
  border-left-color: #17a2b8;
}
.insight-item.warning {
  background: rgba(255, 193, 7, 0.1);
  border-left-color: #ffc107;
}
.insight-item.success {
  background: rgba(40, 167, 69, 0.1);
  border-left-color: #28a745;
}
.insight-icon {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
}
.insight-item.positive .insight-icon {
  background: #28a745;
}
.insight-item.info .insight-icon {
  background: #17a2b8;
}
.insight-item.warning .insight-icon {
  background: #ffc107;
}
.insight-item.success .insight-icon {
  background: #28a745;
}
.insight-content {
  flex: 1;
}
.insight-title {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.insight-description {
  font-size: 0.9rem;
  color: #6c757d;
}
.achievement-badge {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: white;
  padding: 1.5rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
}
.badge-icon {
  font-size: 2rem;
  color: #ffd700;
}
.badge-content h6 {
  margin: 0 0 0.5rem 0;
  color: var(--text-accent);
}
.badge-content p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.9;
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
  .duration-stats {
    flex-direction: column;
  }
  .weekly-pattern {
    height: 150px;
  }
  .day-label {
    font-size: 0.7rem;
  }
  .achievement-badge {
    flex-direction: column;
    text-align: center;
  }
}
</style>