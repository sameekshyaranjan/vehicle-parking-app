<template>
  <div class="user-reports">
    
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h2 class="page-title">
            <i class="fas fa-chart-bar me-2"></i>My Parking Reports
          </h2>
          <p class="page-subtitle">
            Analyze your parking patterns and track your spending
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="header-actions">
            <select v-model="selectedPeriod" class="form-select form-select-sm me-2" style="width: auto; display: inline-block;">
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
              <option value="6m">Last 6 Months</option>
              <option value="1y">Last Year</option>
            </select>
            <button class="btn btn-outline-primary me-2" @click="exportReport">
              <i class="fas fa-download me-1"></i>Export PDF
            </button>
            <button class="btn btn-primary" @click="refreshData">
              <i class="fas fa-sync me-1"></i>Refresh
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div class="summary-section mb-4">
      <div class="row">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="summary-card spending">
            <div class="summary-icon">
              <i class="fas fa-rupee-sign"></i>
            </div>
            <div class="summary-content">
              <h3>₹{{ reportData.totalSpending }}</h3>
              <p>Total Spending</p>
              <div class="summary-change" :class="spendingTrend.type">
                <i class="fas" :class="spendingTrend.icon"></i>
                {{ spendingTrend.percentage }}% vs last period
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="summary-card frequency">
            <div class="summary-icon">
              <i class="fas fa-calendar-alt"></i>
            </div>
            <div class="summary-content">
              <h3>{{ reportData.totalSessions }}</h3>
              <p>Parking Sessions</p>
              <div class="summary-change positive">
                <i class="fas fa-arrow-up"></i>
                {{ reportData.sessionGrowth }}% increase
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="summary-card duration">
            <div class="summary-icon">
              <i class="fas fa-clock"></i>
            </div>
            <div class="summary-content">
              <h3>{{ reportData.avgDuration }}h</h3>
              <p>Avg Duration</p>
              <div class="summary-change neutral">
                <i class="fas fa-minus"></i>
                {{ reportData.durationChange }}% change
              </div>
            </div>
          </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="summary-card savings">
            <div class="summary-icon">
              <i class="fas fa-piggy-bank"></i>
            </div>
            <div class="summary-content">
              <h3>₹{{ reportData.totalSavings }}</h3>
              <p>Money Saved</p>
              <div class="summary-change positive">
                <i class="fas fa-percentage"></i>
                {{ reportData.savingsRate }}% vs street parking
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="charts-section">
      <div class="row">
        
        <div class="col-lg-8">
          <div class="main-charts">
            
            <UserCharts />
          </div>
        </div>
        
        <div class="col-lg-4">
          <div class="insights-sidebar">
            
            <div class="card mb-4">
              <div class="card-header">
                <h6 class="mb-0">
                  <i class="fas fa-chart-pie me-2"></i>Cost Breakdown
                </h6>
              </div>
              <div class="card-body">
                <div class="cost-breakdown">
                  <div
                    v-for="item in costBreakdown"
                    :key="item.category"
                    class="breakdown-item"
                  >
                    <div class="breakdown-info">
                      <div class="breakdown-label">{{ item.category }}</div>
                      <div class="breakdown-amount">₹{{ item.amount }}</div>
                    </div>
                    <div class="breakdown-bar">
                      <div
                        class="bar-fill"
                        :style="{ width: item.percentage + '%', background: item.color }"
                      ></div>
                    </div>
                    <div class="breakdown-percentage">{{ item.percentage }}%</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="card mb-4">
              <div class="card-header">
                <h6 class="mb-0">
                  <i class="fas fa-heart me-2"></i>Most Visited Locations
                </h6>
              </div>
              <div class="card-body">
                <div class="favorite-locations">
                  <div
                    v-for="(location, index) in favoriteLocations"
                    :key="location.id"
                    class="location-item"
                  >
                    <div class="location-rank">{{ index + 1 }}</div>
                    <div class="location-details">
                      <h6>{{ location.name }}</h6>
                      <div class="location-stats">
                        <span>{{ location.visits }} visits</span>
                        <span>₹{{ location.totalSpent }}</span>
                      </div>
                    </div>
                    <div class="location-percentage">{{ location.percentage }}%</div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="card">
              <div class="card-header">
                <h6 class="mb-0">
                  <i class="fas fa-brain me-2"></i>Parking Insights
                </h6>
              </div>
              <div class="card-body">
                <div class="insights-list">
                  <div
                    v-for="insight in parkingInsights"
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="detailed-reports mt-4">
      <div class="card">
        <div class="card-header">
          <div class="d-flex justify-content-between align-items-center">
            <h6 class="mb-0">
              <i class="fas fa-table me-2"></i>Detailed Parking Report
            </h6>
            <div class="report-controls">
              <div class="btn-group btn-group-sm" role="group">
                <input type="radio" class="btn-check" id="weekly-view" v-model="reportView" value="weekly">
                <label class="btn btn-outline-primary" for="weekly-view">Weekly</label>
                <input type="radio" class="btn-check" id="monthly-view" v-model="reportView" value="monthly">
                <label class="btn btn-outline-primary" for="monthly-view">Monthly</label>
                <input type="radio" class="btn-check" id="location-view" v-model="reportView" value="location">
                <label class="btn btn-outline-primary" for="location-view">By Location</label>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body">
          
          <div v-if="reportView === 'weekly'" class="weekly-report">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Week</th>
                    <th>Sessions</th>
                    <th>Total Hours</th>
                    <th>Amount Spent</th>
                    <th>Avg Cost/Hour</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="week in weeklyData" :key="week.week">
                    <td>{{ week.week }}</td>
                    <td>{{ week.sessions }}</td>
                    <td>{{ week.hours }}h</td>
                    <td>₹{{ week.amount }}</td>
                    <td>₹{{ week.avgCost }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div v-if="reportView === 'monthly'" class="monthly-report">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Month</th>
                    <th>Sessions</th>
                    <th>Total Hours</th>
                    <th>Amount Spent</th>
                    <th>Growth</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="month in monthlyData" :key="month.month">
                    <td>{{ month.month }}</td>
                    <td>{{ month.sessions }}</td>
                    <td>{{ month.hours }}h</td>
                    <td>₹{{ month.amount }}</td>
                    <td>
                      <span class="badge" :class="getGrowthClass(month.growth)">
                        {{ month.growth > 0 ? '+' : '' }}{{ month.growth }}%
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div v-if="reportView === 'location'" class="location-report">
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Location</th>
                    <th>Visits</th>
                    <th>Total Hours</th>
                    <th>Amount Spent</th>
                    <th>Avg Duration</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="location in locationData" :key="location.name">
                    <td>{{ location.name }}</td>
                    <td>{{ location.visits }}</td>
                    <td>{{ location.hours }}h</td>
                    <td>₹{{ location.amount }}</td>
                    <td>{{ location.avgDuration }}h</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="goals-section mt-4">
      <div class="card">
        <div class="card-header">
          <h6 class="mb-0">
            <i class="fas fa-target me-2"></i>Monthly Goals & Targets
          </h6>
        </div>
        <div class="card-body">
          <div class="row">
            <div class="col-md-6">
              <div class="goal-item">
                <div class="goal-header">
                  <span class="goal-title">Spending Budget</span>
                  <span class="goal-value">₹{{ goals.spendingBudget }}</span>
                </div>
                <div class="goal-progress">
                  <div class="progress">
                    <div
                      class="progress-bar"
                      :class="getProgressClass(goals.spendingProgress)"
                      :style="{ width: goals.spendingProgress + '%' }"
                    ></div>
                  </div>
                  <small>{{ goals.spendingProgress }}% of ₹{{ goals.spendingBudget }}</small>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="goal-item">
                <div class="goal-header">
                  <span class="goal-title">Parking Sessions</span>
                  <span class="goal-value">{{ goals.sessionTarget }}</span>
                </div>
                <div class="goal-progress">
                  <div class="progress">
                    <div
                      class="progress-bar bg-info"
                      :style="{ width: goals.sessionProgress + '%' }"
                    ></div>
                  </div>
                  <small>{{ Math.round(goals.sessionProgress * goals.sessionTarget / 100) }} of {{ goals.sessionTarget }} sessions</small>
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
import { ref, computed, onMounted } from 'vue'
import { useParkingStore } from '../../store/modules/parking'
import UserCharts from '../../components/user/UserCharts.vue'
export default {
  name: 'UserReports',
  components: {
    UserCharts
  },
  setup() {
    const parkingStore = useParkingStore()
    const selectedPeriod = ref('30d')
    const reportView = ref('weekly')
    const reportData = ref({
      totalSpending: 3200,
      totalSessions: 28,
      avgDuration: 3.2,
      totalSavings: 850,
      sessionGrowth: 12,
      durationChange: -5,
      savingsRate: 21
    })
    const costBreakdown = ref([
      { category: 'Shopping Malls', amount: 1200, percentage: 37, color: '#4B006E' },
      { category: 'Office Areas', amount: 980, percentage: 31, color: '#8AB8FE' },
      { category: 'Airports', amount: 640, percentage: 20, color: '#000133' },
      { category: 'Metro Stations', amount: 380, percentage: 12, color: '#6c757d' }
    ])
    const favoriteLocations = ref([
      { id: 1, name: 'Central Mall', visits: 12, totalSpent: 600, percentage: 42 },
      { id: 2, name: 'Office Complex', visits: 8, totalSpent: 400, percentage: 29 },
      { id: 3, name: 'Metro Station', visits: 5, totalSpent: 250, percentage: 18 },
      { id: 4, name: 'Airport Terminal', visits: 3, totalSpent: 150, percentage: 11 }
    ])
    const parkingInsights = ref([
      {
        id: 1,
        type: 'positive',
        icon: 'fa-thumbs-up',
        title: 'Smart Saver!',
        description: 'You consistently book during off-peak hours, saving 15% on average.'
      },
      {
        id: 2,
        type: 'info',
        icon: 'fa-clock',
        title: 'Duration Optimizer',
        description: 'Your average parking duration has decreased by 20 minutes.'
      },
      {
        id: 3,
        type: 'warning',
        icon: 'fa-chart-line',
        title: 'Budget Alert',
        description: 'You\'re 85% through your monthly parking budget.'
      }
    ])
    const weeklyData = ref([
      { week: 'Week 1', sessions: 7, hours: 24, amount: 800, avgCost: 33 },
      { week: 'Week 2', sessions: 6, hours: 20, amount: 700, avgCost: 35 },
      { week: 'Week 3', sessions: 8, hours: 28, amount: 900, avgCost: 32 },
      { week: 'Week 4', sessions: 7, hours: 22, amount: 750, avgCost: 34 }
    ])
    const monthlyData = ref([
      { month: 'January', sessions: 25, hours: 80, amount: 2800, growth: 12 },
      { month: 'February', sessions: 28, hours: 84, amount: 3200, growth: 14 },
      { month: 'March', sessions: 22, hours: 70, amount: 2600, growth: -12 },
      { month: 'April', sessions: 30, hours: 95, amount: 3500, growth: 36 }
    ])
    const locationData = ref([
      { name: 'Central Mall', visits: 12, hours: 36, amount: 1200, avgDuration: 3.0 },
      { name: 'Office Complex', visits: 8, hours: 32, amount: 980, avgDuration: 4.0 },
      { name: 'Metro Station', visits: 5, hours: 10, amount: 380, avgDuration: 2.0 },
      { name: 'Airport Terminal', visits: 3, hours: 24, amount: 640, avgDuration: 8.0 }
    ])
    const goals = ref({
      spendingBudget: 4000,
      spendingProgress: 80,
      sessionTarget: 35,
      sessionProgress: 80
    })
    const spendingTrend = computed(() => {
      const change = reportData.value.sessionGrowth
      return {
        type: change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral',
        icon: change > 0 ? 'fa-arrow-up' : change < 0 ? 'fa-arrow-down' : 'fa-minus',
        percentage: Math.abs(change)
      }
    })
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
    const exportReport = () => {
      console.log('Exporting user report as PDF...')
      parkingStore.exportUserReport(selectedPeriod.value)
    }
    const refreshData = async () => {
      console.log('Refreshing report data...')
      await parkingStore.fetchUserReports(selectedPeriod.value)
    }
    onMounted(() => {
      refreshData()
    })
    return {
      selectedPeriod,
      reportView,
      reportData,
      costBreakdown,
      favoriteLocations,
      parkingInsights,
      weeklyData,
      monthlyData,
      locationData,
      goals,
      spendingTrend,
      getGrowthClass,
      getProgressClass,
      exportReport,
      refreshData
    }
  }
}
</script>
<style scoped>
.user-reports {
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
.btn-check:checked + .btn-outline-primary {
  background-color: var(--secondary-color);
  border-color: var(--secondary-color);
  color: white;
}
.summary-card {
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}
.summary-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 1, 51, 0.15);
}
.summary-icon {
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
.summary-card.spending .summary-icon {
  background: linear-gradient(135deg, #28a745, #20c997);
}
.summary-card.frequency .summary-icon {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.summary-card.duration .summary-icon {
  background: linear-gradient(135deg, #fd7e14, #f8b500);
}
.summary-card.savings .summary-icon {
  background: linear-gradient(135deg, #6f42c1, #e83e8c);
}
.summary-content h3 {
  color: var(--primary-color);
  font-weight: 700;
  margin-bottom: 0.25rem;
  font-size: 1.75rem;
}
.summary-content p {
  color: #6c757d;
  margin-bottom: 0.5rem;
}
.summary-change {
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}
.summary-change.positive {
  color: #28a745;
}
.summary-change.negative {
  color: #dc3545;
}
.summary-change.neutral {
  color: #6c757d;
}
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
}
.card-header {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border-radius: 15px 15px 0 0 !important;
  padding: 1.25rem;
}
.card-header h6 {
  color: var(--primary-color);
  font-weight: 600;
  margin: 0;
}
.breakdown-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}
.breakdown-item:last-child {
  margin-bottom: 0;
}
.breakdown-info {
  flex: 0 0 120px;
  margin-right: 1rem;
}
.breakdown-label {
  font-size: 0.9rem;
  color: var(--primary-color);
  font-weight: 500;
}
.breakdown-amount {
  font-size: 0.8rem;
  color: #6c757d;
}
.breakdown-bar {
  flex: 1;
  height: 8px;
  background: rgba(138, 184, 254, 0.2);
  border-radius: 4px;
  margin-right: 1rem;
  overflow: hidden;
}
.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}
.breakdown-percentage {
  flex: 0 0 40px;
  text-align: right;
  font-size: 0.9rem;
  color: var(--secondary-color);
  font-weight: 600;
}
.location-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
  margin-bottom: 1rem;
}
.location-item:last-child {
  margin-bottom: 0;
}
.location-rank {
  width: 30px;
  height: 30px;
  background: var(--secondary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  margin-right: 1rem;
}
.location-details {
  flex: 1;
}
.location-details h6 {
  color: var(--primary-color);
  font-weight: 600;
  margin-bottom: 0.25rem;
}
.location-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #6c757d;
}
.location-percentage {
  color: var(--secondary-color);
  font-weight: 600;
}
.insight-item {
  display: flex;
  align-items: flex-start;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  border-left: 4px solid;
}
.insight-item:last-child {
  margin-bottom: 0;
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
.insight-icon {
  width: 35px;
  height: 35px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  margin-right: 0.75rem;
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
.table {
  background: white;
  border-radius: 10px;
  overflow: hidden;
}
.table th {
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: none;
  font-weight: 600;
  color: var(--primary-color);
}
.table td {
  border-bottom: 1px solid rgba(138, 184, 254, 0.1);
  vertical-align: middle;
}
.table tbody tr:hover {
  background-color: rgba(138, 184, 254, 0.05);
}
.goal-item {
  background: rgba(138, 184, 254, 0.05);
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}
.goal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.goal-title {
  color: var(--primary-color);
  font-weight: 600;
}
.goal-value {
  color: var(--secondary-color);
  font-weight: 700;
  font-size: 1.1rem;
}
.goal-progress .progress {
  height: 8px;
  border-radius: 4px;
  background: rgba(138, 184, 254, 0.2);
  margin-bottom: 0.5rem;
}
.goal-progress .progress-bar {
  border-radius: 4px;
}
.goal-progress small {
  color: #6c757d;
}
@media (max-width: 768px) {
  .user-reports {
    padding: 1rem;
  }
  .header-actions {
    margin-top: 1rem;
  }
  .form-select {
    width: 100% !important;
    margin-bottom: 0.5rem;
  }
  .breakdown-item {
    flex-direction: column;
    align-items: flex-start;
  }
  .breakdown-info {
    margin-bottom: 0.5rem;
  }
  .breakdown-bar {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  .location-item {
    flex-direction: column;
    text-align: center;
  }
  .location-details {
    margin: 1rem 0;
  }
}
</style>