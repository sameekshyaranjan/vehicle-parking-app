import { BaseApiService } from './api.js'
class UserService extends BaseApiService {
  constructor() {
    super('/user')
  }
  async getDashboard() {
    const response = await this.get('/dashboard')
    return {
      stats: response.data.stats,
      activeBooking: response.data.active_booking,
      recentBookings: response.data.recent_bookings,
      favoriteLocations: response.data.favorite_locations,
      notifications: response.data.notifications
    }
  }
  async getUserStats(timeRange = '30d') {
    const response = await this.get('/stats', { time_range: timeRange })
    return response.data.stats
  }
  async updatePreferences(preferences) {
    const response = await this.patch('/preferences', preferences)
    return {
      preferences: response.data.preferences,
      message: response.data.message || 'Preferences updated successfully'
    }
  }
  async searchParkingLots(searchCriteria) {
    const params = {
      location: searchCriteria.location?.trim() || '',
      latitude: searchCriteria.latitude || '',
      longitude: searchCriteria.longitude || '',
      date: searchCriteria.date || '',
      time: searchCriteria.time || '',
      duration: searchCriteria.duration || '',
      max_distance: searchCriteria.maxDistance || 10,
      min_price: searchCriteria.minPrice || '',
      max_price: searchCriteria.maxPrice || '',
      features: searchCriteria.features || [],
      sort_by: searchCriteria.sortBy || 'distance'
    }
    const response = await this.get('/parking-lots/search', params)
    return {
      lots: response.data.parking_lots,
      total: response.data.total,
      searchId: response.data.search_id
    }
  }
  async getNearbyLots(latitude, longitude, radius = 5) {
    const response = await this.get('/parking-lots/nearby', {
      latitude: latitude,
      longitude: longitude,
      radius: radius
    })
    return response.data.parking_lots
  }
  async getParkingLotDetails(lotId) {
    const response = await this.get(`/parking-lots/${lotId}`)
    return {
      lot: response.data.parking_lot,
      availability: response.data.availability,
      pricing: response.data.pricing,
      features: response.data.features,
      reviews: response.data.reviews
    }
  }
  async getRealTimeAvailability(lotId, date, time) {
    const response = await this.get(`/parking-lots/${lotId}/availability`, {
      date: date,
      time: time
    })
    return {
      available: response.data.available,
      spots: response.data.spots,
      estimatedWait: response.data.estimated_wait
    }
  }
  async createBooking(bookingData) {
    const response = await this.post('/bookings', {
      lot_id: bookingData.lotId,
      vehicle_number: bookingData.vehicleNumber.trim().toUpperCase(),
      parking_datetime: bookingData.parkingDateTime,
      expected_duration: parseInt(bookingData.expectedDuration),
      estimated_cost: parseFloat(bookingData.estimatedCost),
      remarks: bookingData.remarks?.trim() || '',
      payment_method: bookingData.paymentMethod || 'cash'
    })
    return {
      booking: response.data.booking,
      bookingId: response.data.booking_id,
      message: response.data.message || 'Booking created successfully'
    }
  }
  async getBookings(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      status: filters.status || '',
      date_from: filters.dateFrom || '',
      date_to: filters.dateTo || '',
      sort_by: filters.sortBy || 'parking_timestamp',
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
  async getActiveBooking() {
    const response = await this.get('/bookings/active')
    return response.data.booking
  }
  async extendBooking(bookingId, additionalHours) {
    const response = await this.post(`/bookings/${bookingId}/extend`, {
      additional_hours: parseInt(additionalHours)
    })
    return {
      booking: response.data.booking,
      additionalCost: response.data.additional_cost,
      newEndTime: response.data.new_end_time,
      message: response.data.message || 'Booking extended successfully'
    }
  }
  async releaseBooking(bookingId, releaseData) {
    const response = await this.post(`/bookings/${bookingId}/release`, {
      leaving_timestamp: releaseData.leavingTimestamp,
      rating: releaseData.rating || 5,
      feedback: releaseData.feedback?.trim() || '',
      vehicle_condition: releaseData.vehicleCondition || 'good'
    })
    return {
      booking: response.data.booking,
      finalCost: response.data.final_cost,
      duration: response.data.actual_duration,
      receiptId: response.data.receipt_id,
      message: response.data.message || 'Booking completed successfully'
    }
  }
  async cancelBooking(bookingId, reason) {
    const response = await this.post(`/bookings/${bookingId}/cancel`, {
      reason: reason.trim()
    })
    return {
      booking: response.data.booking,
      refundAmount: response.data.refund_amount,
      cancellationFee: response.data.cancellation_fee,
      message: response.data.message || 'Booking cancelled successfully'
    }
  }
  async addToFavorites(lotId, name = '') {
    const response = await this.post('/favorites', {
      lot_id: lotId,
      custom_name: name.trim()
    })
    return {
      favorite: response.data.favorite,
      message: response.data.message || 'Added to favorites'
    }
  }
  async removeFromFavorites(lotId) {
    const response = await this.delete(`/favorites/${lotId}`)
    return {
      message: response.data.message || 'Removed from favorites'
    }
  }
  async getFavoriteLocations() {
    const response = await this.get('/favorites')
    return response.data.favorites
  }
  async getBookingHistory(timeRange = '6m') {
    const response = await this.get('/bookings/history', {
      time_range: timeRange
    })
    return {
      bookings: response.data.bookings,
      analytics: response.data.analytics,
      patterns: response.data.patterns
    }
  }
  async getPaymentMethods() {
    const response = await this.get('/payment-methods')
    return response.data.payment_methods
  }
  async addPaymentMethod(paymentData) {
    const response = await this.post('/payment-methods', paymentData)
    return {
      paymentMethod: response.data.payment_method,
      message: response.data.message || 'Payment method added'
    }
  }
  async removePaymentMethod(paymentMethodId) {
    const response = await this.delete(`/payment-methods/${paymentMethodId}`)
    return {
      message: response.data.message || 'Payment method removed'
    }
  }
  async getBillingHistory(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      date_from: filters.dateFrom || '',
      date_to: filters.dateTo || ''
    }
    const response = await this.get('/billing/history', params)
    return {
      transactions: response.data.transactions,
      pagination: response.data.pagination,
      summary: response.data.summary
    }
  }
  async downloadReceipt(bookingId, filename = null) {
    return await this.download(`/bookings/${bookingId}/receipt`, {}, filename)
  }
  async getNotifications(filters = {}) {
    const params = {
      page: filters.page || 1,
      per_page: filters.perPage || 20,
      type: filters.type || '',
      read: filters.read !== undefined ? filters.read : ''
    }
    const response = await this.get('/notifications', params)
    return {
      notifications: response.data.notifications,
      pagination: response.data.pagination,
      unreadCount: response.data.unread_count
    }
  }
  async markNotificationRead(notificationId) {
    const response = await this.patch(`/notifications/${notificationId}/read`)
    return {
      message: response.data.message || 'Notification marked as read'
    }
  }
  async markAllNotificationsRead() {
    const response = await this.post('/notifications/mark-all-read')
    return {
      marked: response.data.marked,
      message: response.data.message || 'All notifications marked as read'
    }
  }
  async deleteNotification(notificationId) {
    const response = await this.delete(`/notifications/${notificationId}`)
    return {
      message: response.data.message || 'Notification deleted'
    }
  }
  async updateNotificationPreferences(preferences) {
    const response = await this.patch('/notifications/preferences', preferences)
    return {
      preferences: response.data.preferences,
      message: response.data.message || 'Notification preferences updated'
    }
  }
  async getUserReports(timeRange = '30d') {
    const response = await this.get('/reports', { time_range: timeRange })
    return response.data
  }
  async exportUserData(format = 'csv') {
    return await this.download('/export', { format: format }, `parking_data.${format}`)
  }
  async getParkingPatterns() {
    const response = await this.get('/analytics/patterns')
    return response.data.patterns
  }
  async getSpendingAnalysis(timeRange = '6m') {
    const response = await this.get('/analytics/spending', {
      time_range: timeRange
    })
    return response.data.analysis
  }
  async getVehicles() {
    const response = await this.get('/vehicles')
    return response.data.vehicles
  }
  async addVehicle(vehicleData) {
    const response = await this.post('/vehicles', {
      vehicle_number: vehicleData.vehicleNumber.trim().toUpperCase(),
      vehicle_type: vehicleData.vehicleType || 'car',
      make: vehicleData.make?.trim() || '',
      model: vehicleData.model?.trim() || '',
      color: vehicleData.color?.trim() || '',
      is_default: vehicleData.isDefault || false
    })
    return {
      vehicle: response.data.vehicle,
      message: response.data.message || 'Vehicle added successfully'
    }
  }
  async updateVehicle(vehicleId, vehicleData) {
    const response = await this.put(`/vehicles/${vehicleId}`, vehicleData)
    return {
      vehicle: response.data.vehicle,
      message: response.data.message || 'Vehicle updated successfully'
    }
  }
  async removeVehicle(vehicleId) {
    const response = await this.delete(`/vehicles/${vehicleId}`)
    return {
      message: response.data.message || 'Vehicle removed successfully'
    }
  }
  async setDefaultVehicle(vehicleId) {
    const response = await this.patch(`/vehicles/${vehicleId}/default`)
    return {
      vehicle: response.data.vehicle,
      message: response.data.message || 'Default vehicle updated'
    }
  }
  async submitReview(lotId, reviewData) {
    const response = await this.post(`/parking-lots/${lotId}/review`, {
      rating: parseInt(reviewData.rating),
      comment: reviewData.comment?.trim() || '',
      tags: reviewData.tags || []
    })
    return {
      review: response.data.review,
      message: response.data.message || 'Review submitted successfully'
    }
  }
  async getUserReviews() {
    const response = await this.get('/reviews')
    return response.data.reviews
  }
  async updateReview(reviewId, reviewData) {
    const response = await this.put(`/reviews/${reviewId}`, reviewData)
    return {
      review: response.data.review,
      message: response.data.message || 'Review updated successfully'
    }
  }
  async deleteReview(reviewId) {
    const response = await this.delete(`/reviews/${reviewId}`)
    return {
      message: response.data.message || 'Review deleted successfully'
    }
  }
}
const userService = new UserService()
export default userService
export { UserService }