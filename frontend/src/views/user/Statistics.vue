<template>
  <div class="user-statistics">
    <div class="page-header mb-4">
      <div class="row align-items-center">
        <div class="col-md-6">
          <h2 class="page-title">
            <i class="fas fa-chart-bar me-2"></i>
            My Statistics
          </h2>
          <p class="page-subtitle">
            Analyze your parking usage and spending patterns
          </p>
        </div>
        <div class="col-md-6 text-md-end">
          <div class="header-actions">
            <select v-model="timeRange" class="form-select form-select-sm me-2" style="width:auto;">
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="90d">Last 90 Days</option>
            </select>
            <button class="btn btn-outline-secondary me-2" @click="refresh">
              <i class="fas fa-sync-alt"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div class="summary-cards mb-4">
      <div class="row">
        <div class="col-md-3 mb-3" v-for="card in cards" :key="card.label">
          <div class="card summary-card">
            <div class="card-body d-flex align-items-center">
              <div class="icon-wrapper me-3" :style="{ background: card.color }">
                <i :class="['fas', card.icon]"></i>
              </div>
              <div>
                <h4 class="mb-1">{{ card.value }}</h4>
                <p class="mb-0">{{ card.label }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="charts-section">
      <div class="row">
        <div class="col-lg-4 mb-4">
          <div class="card">
            <div class="card-header">
              <h6 class="mb-0"><i class="fas fa-chart-pie me-2"></i> Cost Breakdown</h6>
            </div>
            <div class="card-body">
              <div v-for="segment in costBreakdown" :key="segment.category" class="mb-3">
                <div class="d-flex justify-content-between">
                  <span>{{ segment.category }}</span>
                  <span>₹{{ segment.amount }}</span>
                </div>
                <div class="progress" style="height:6px;">
                  <div
                    class="progress-bar"
                    :style="{ width: segment.percent + '%', background: segment.color }"
                  ></div>
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
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/modules/user'
import UserCharts from '@/components/user/UserCharts.vue'
export default {
  name: 'UserStatistics',
  components: {
    UserCharts
  },
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    const selectedPeriod = ref('30d')
    const reportView = ref('weekly')
    const reportData = computed(() => userStore.reportData)
    const costBreakdown = computed(() => userStore.costBreakdown)
    const favoriteLocations = computed(() => userStore.topLocations)
    const parkingInsights = computed(() => userStore.parkingInsights)
    const weeklyData = computed(() => userStore.weeklyData)
    const monthlyData = computed(() => userStore.monthlyData)
    const locationData = computed(() => userStore.locationData)
    const isLoading = computed(() => userStore.isLoading)
    const error = computed(() => userStore.error)
    const spendingTrend = computed(() => userStore.spendingTrend)
    const cards = computed(() => [
      {
        label: 'Total Sessions',
        value: userStore.formatNumber(reportData.value.totalSessions),
        icon: 'fa-calendar-alt',
        color: '#000133'
      },
      {
        label: 'Total Hours',
        value: `${reportData.value.avgDuration * reportData.value.totalSessions}h`,
        icon: 'fa-clock',
        color: '#4B006E'
      },
      {
        label: 'Total Spent',
        value: `₹${userStore.formatNumber(reportData.value.totalSpending)}`,
        icon: 'fa-rupee-sign',
        color: '#8AB8FE'
      },
      {
        label: 'Savings',
        value: `₹${userStore.formatNumber(reportData.value.totalSavings)}`,
        icon: 'fa-piggy-bank',
        color: '#4B006E'
      }
    ])
    const goals = ref({
      spendingBudget: 4000,
      spendingProgress: 80,
      sessionTarget: 35,
      sessionProgress: 80
    })
    const refresh = async () => {
      try {
        await userStore.fetchUserReports(selectedPeriod.value)
      } catch (error) {
        console.error('Error refreshing statistics:', error)
      }
    }
    const exportReport = async () => {
      try {
        const result = await userStore.exportUserReport(selectedPeriod.value)
        console.log('Export initiated:', result)
      } catch (error) {
        console.error('Error exporting report:', error)
      }
    }
    const getRankClass = (index) => {
      const classes = ['rank-first', 'rank-second', 'rank-third']
      return classes[index] || 'rank-other'
    }
    const getGrowthClass = (growth) => {
      return userStore.getGrowthClass(growth)
    }
    const getProgressClass = (progress) => {
      return userStore.getProgressClass(progress)
    }
    const formatNumber = (num) => {
      return userStore.formatNumber(num)
    }
    watch(selectedPeriod, async (newPeriod) => {
      await refresh()
    })
    onMounted(async () => {
      try {
        await userStore.fetchUserReports(selectedPeriod.value)
      } catch (error) {
        console.error('Error loading statistics:', error)
      }
    })
    return {
      reportData,
      costBreakdown,
      favoriteLocations,
      parkingInsights,
      weeklyData,
      monthlyData,
      locationData,
      isLoading,
      error,
      selectedPeriod,
      reportView,
      goals,
      spendingTrend,
      cards,
      refresh,
      exportReport,
      getRankClass,
      getGrowthClass,
      getProgressClass,
      formatNumber
    }
  }
}
</script>
<style scoped>
.user-statistics {
  padding: 1.5rem;
}
.page-title {
  color: #e23e3e;
  font-weight: 700;
}
.page-subtitle {
  color: #4B006E;
}
.summary-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,1,51,0.1);
}
.icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
.btn-primary {
  background: linear-gradient(135deg, #8AB8FE, #4B006E);
  border: none;
}
.btn-outline-secondary {
  color: #4B006E;
  border-color: #4B006E;
}
.btn-outline-secondary:hover {
  background-color: rgba(75,0,110,0.1);
}
.card {
  border: none;
  border-radius: 12px;
}
.card-header {
  background: #f8f9fa;
  border-radius: 12px 12px 0 0;
  font-weight: 600;
  color: #000133;
}
.progress {
  background: #e9ecef;
}
.progress-bar {
  transition: width 0.6s ease;
}
@media (max-width: 768px) {
  .page-header .header-actions {
    margin-top: 1rem;
  }
}
</style>