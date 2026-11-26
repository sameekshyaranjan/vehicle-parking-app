import { BaseApiService } from './api.js'
class AdminService extends BaseApiService {
  constructor() {
    super('/admin')
  }
  async getDashboard() {
    const response = await this.get('/dashboard')
    return {
      stats: response.data.stats,
      charts: response.data.charts,
      recentActivity: response.data.recent_activity,
      alerts: response.data.alerts
    }
  }
  async getStatistics(timeRange = '30d') {
    const response = await this.get('/statistics', { time_range: timeRange })
    return response.data
  }
  async getRealTimeMetrics() {
    const response = await this.get('/metrics/realtime')
    return response.data.metrics
  }
  async getParkingLots(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      search: filters.search || '',
      status: filters.status || '',
      sort_by: filters.sortBy || 'created_at',
      sort_order: filters.sortOrder || 'desc'
    }
    const response = await this.get('/parking-lots', params)
    return {
      lots: response.data.parking_lots,
      pagination: response.data.pagination,
      total: response.data.total
    }
  }
  async getParkingLot(lotId) {
    const response = await this.get(`/parking-lots/${lotId}`)
    return response.data.parking_lot
  }
  async createParkingLot(lotData) {
    const response = await this.post('/parking-lots', {
      prime_location_name: lotData.prime_location_name.trim(),
      address: lotData.address.trim(),
      pin_code: lotData.pin_code.trim(),
      price: parseFloat(lotData.price),
      number_of_spots: parseInt(lotData.number_of_spots)
    })
    return {
      lot: response.data.parking_lot,
      message: response.data.message || 'Parking lot created successfully'
    }
  }
  async updateParkingLot(lotId, lotData) {
    const response = await this.put(`/parking-lots/${lotId}`, {
      prime_location_name: lotData.prime_location_name?.trim(),
      address: lotData.address?.trim(),
      pin_code: lotData.pin_code?.trim(),
      price: lotData.price ? parseFloat(lotData.price) : undefined,
      number_of_spots: lotData.number_of_spots ? parseInt(lotData.number_of_spots) : undefined
    })
    return {
      lot: response.data.parking_lot,
      message: response.data.message || 'Parking lot updated successfully'
    }
  }
  async deleteParkingLot(lotId) {
    const response = await this.delete(`/parking-lots/${lotId}`)
    return {
      message: response.data.message || 'Parking lot deleted successfully'
    }
  }
  async bulkUpdateParkingLots(lotIds, action, data = {}) {
    const response = await this.post('/parking-lots/bulk', {
      lot_ids: lotIds,
      action: action,
      data: data
    })
    return {
      updated: response.data.updated,
      message: response.data.message || 'Bulk operation completed'
    }
  }
  async getParkingSpots(lotId, filters = {}) {
    const params = {
      status: filters.status || '',
      floor: filters.floor || '',
      section: filters.section || ''
    }
    const response = await this.get(`/parking-lots/${lotId}/spots`, params)
    return {
      spots: response.data.spots,
      layout: response.data.layout,
      summary: response.data.summary
    }
  }
  async updateSpotStatus(lotId, spotId, status, reason = '') {
    const response = await this.patch(`/parking-lots/${lotId}/spots/${spotId}`, {
      status: status,
      reason: reason
    })
    return {
      spot: response.data.spot,
      message: response.data.message || 'Spot status updated'
    }
  }
  async bulkUpdateSpots(lotId, spotIds, action, data = {}) {
    const response = await this.post(`/parking-lots/${lotId}/spots/bulk`, {
      spot_ids: spotIds,
      action: action,
      data: data
    })
    return {
      updated: response.data.updated,
      message: response.data.message || 'Spots updated successfully'
    }
  }
  async getUsers(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      search: filters.search || '',
      status: filters.status || '',
      role: filters.role || '',
      sort_by: filters.sortBy || 'created_at',
      sort_order: filters.sortOrder || 'desc'
    }
    const response = await this.get('/users', params)
    return {
      users: response.data.users,
      pagination: response.data.pagination,
      total: response.data.total
    }
  }
  async getUser(userId) {
    const response = await this.get(`/users/${userId}`)
    return {
      user: response.data.user,
      stats: response.data.stats,
      recentActivity: response.data.recent_activity
    }
  }
  async createUser(userData) {
    const response = await this.post('/users', {
      username: userData.username.trim(),
      email: userData.email.trim().toLowerCase(),
      fullname: userData.fullname.trim(),
      password: userData.password,
      role: userData.role || 'user',
      is_active: userData.is_active !== false
    })
    return {
      user: response.data.user,
      message: response.data.message || 'User created successfully'
    }
  }
  async updateUser(userId, userData) {
    const response = await this.put(`/users/${userId}`, userData)
    return {
      user: response.data.user,
      message: response.data.message || 'User updated successfully'
    }
  }
  async toggleUserStatus(userId, isActive, reason = '') {
    const response = await this.patch(`/users/${userId}/status`, {
      is_active: isActive,
      reason: reason
    })
    return {
      user: response.data.user,
      message: response.data.message || 'User status updated'
    }
  }
  async deleteUser(userId) {
    const response = await this.delete(`/users/${userId}`)
    return {
      message: response.data.message || 'User deleted successfully'
    }
  }
  async sendUserMessage(userId, messageData) {
    const response = await this.post(`/users/${userId}/message`, {
      subject: messageData.subject.trim(),
      message: messageData.message.trim(),
      type: messageData.type || 'info'
    })
    return {
      message: response.data.message || 'Message sent successfully'
    }
  }
  async bulkUserOperation(userIds, action, data = {}) {
    const response = await this.post('/users/bulk', {
      user_ids: userIds,
      action: action,
      data: data
    })
    return {
      processed: response.data.processed,
      message: response.data.message || 'Bulk operation completed'
    }
  }
  async getBookings(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      status: filters.status || '',
      user_id: filters.userId || '',
      lot_id: filters.lotId || '',
      date_from: filters.dateFrom || '',
      date_to: filters.dateTo || '',
      sort_by: filters.sortBy || 'created_at',
      sort_order: filters.sortOrder || 'desc'
    }
    const response = await this.get('/bookings', params)
    return {
      bookings: response.data.bookings,
      pagination: response.data.pagination,
      summary: response.data.summary
    }
  }
  async getBooking(bookingId) {
    const response = await this.get(`/bookings/${bookingId}`)
    return response.data.booking
  }
  async updateBookingStatus(bookingId, status, reason = '') {
    const response = await this.patch(`/bookings/${bookingId}/status`, {
      status: status,
      reason: reason
    })
    return {
      booking: response.data.booking,
      message: response.data.message || 'Booking status updated'
    }
  }
  async forceReleaseBooking(bookingId, reason) {
    const response = await this.post(`/bookings/${bookingId}/force-release`, {
      reason: reason.trim()
    })
    return {
      booking: response.data.booking,
      message: response.data.message || 'Booking released successfully'
    }
  }
  async getRevenueStats(timeRange = '30d', groupBy = 'day') {
    const response = await this.get('/revenue/stats', {
      time_range: timeRange,
      group_by: groupBy
    })
    return response.data
  }
  async generateReport(reportType, params = {}) {
    const response = await this.post('/reports/generate', {
      type: reportType,
      params: params
    })
    return {
      reportId: response.data.report_id,
      message: response.data.message || 'Report generation started'
    }
  }
  async getReportStatus(reportId) {
    const response = await this.get(`/reports/${reportId}/status`)
    return {
      status: response.data.status,
      progress: response.data.progress,
      downloadUrl: response.data.download_url
    }
  }
  async downloadReport(reportId, filename = null) {
    return await this.download(`/reports/${reportId}/download`, {}, filename)
  }
  async getSystemHealth() {
    const response = await this.get('/system/health')
    return response.data
  }
  async getSystemLogs(filters = {}) {
    const params = {
      level: filters.level || '',
      service: filters.service || '',
      date_from: filters.dateFrom || '',
      date_to: filters.dateTo || '',
      page: filters.page || 1,
      per_page: filters.perPage || 50
    }
    const response = await this.get('/system/logs', params)
    return {
      logs: response.data.logs,
      pagination: response.data.pagination
    }
  }
  async updateSystemSettings(settings) {
    const response = await this.patch('/system/settings', settings)
    return {
      settings: response.data.settings,
      message: response.data.message || 'Settings updated successfully'
    }
  }
  async createBackup() {
    const response = await this.post('/system/backup')
    return {
      backupId: response.data.backup_id,
      message: response.data.message || 'Backup initiated'
    }
  }
  async getBackups() {
    const response = await this.get('/system/backups')
    return response.data.backups
  }
  async sendBulkNotification(notificationData) {
    const response = await this.post('/notifications/bulk', {
      title: notificationData.title.trim(),
      message: notificationData.message.trim(),
      type: notificationData.type || 'info',
      target_users: notificationData.targetUsers || 'all',
      user_ids: notificationData.userIds || [],
      scheduled_at: notificationData.scheduledAt || null
    })
    return {
      notificationId: response.data.notification_id,
      message: response.data.message || 'Notification sent successfully'
    }
  }
  async getNotificationAnalytics() {
    const response = await this.get('/notifications/analytics')
    return response.data
  }
}
const adminService = new AdminService()
export default adminService
export { AdminService }