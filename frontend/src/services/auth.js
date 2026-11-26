import { BaseApiService } from './api.js'
class AuthService extends BaseApiService {
  constructor() {
    super('/auth')
  }
  async login(credentials) {
    const response = await this.post('/login', {
      username: credentials.username.trim(),
      password: credentials.password
    })
    return {
      user: response.data.user,
      token: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresIn: response.data.expires_in,
      tokenType: response.data.token_type || 'Bearer'
    }
  }
  async register(userData) {
    const response = await this.post('/register', {
      username: userData.username.trim(),
      email: userData.email.trim().toLowerCase(),
      password: userData.password,
      fullname: userData.fullname.trim(),
      address: userData.address.trim(),
      pin_code: userData.pin_code.trim(),
      phone: userData.phone?.trim() || null
    })
    return {
      user: response.data.user,
      token: response.data.access_token,
      refreshToken: response.data.refresh_token,
      message: response.data.message || 'Registration successful'
    }
  }
  async refreshToken(refreshToken) {
    const response = await this.post('/refresh', {
      refresh_token: refreshToken
    })
    return {
      token: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresIn: response.data.expires_in,
      user: response.data.user
    }
  }
  async logout(token) {
    try {
      await this.post('/logout', {}, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      return { success: true, message: 'Logged out successfully' }
    } catch (error) {
      console.warn('Logout error:', error.message)
      return { success: true, message: 'Logged out locally' }
    }
  }
  async getCurrentUser() {
    const response = await this.get('/me')
    return response.data.user
  }
  async updateProfile(userData) {
    const response = await this.patch('/profile', {
      fullname: userData.fullname?.trim(),
      email: userData.email?.trim().toLowerCase(),
      phone: userData.phone?.trim() || null,
      address: userData.address?.trim(),
      pin_code: userData.pin_code?.trim()
    })
    return {
      user: response.data.user,
      message: response.data.message || 'Profile updated successfully'
    }
  }
  async changePassword(passwordData) {
    const response = await this.post('/change-password', {
      current_password: passwordData.currentPassword,
      new_password: passwordData.newPassword
    })
    return {
      message: response.data.message || 'Password changed successfully'
    }
  }
  async forgotPassword(email) {
    const response = await this.post('/forgot-password', {
      email: email.trim().toLowerCase()
    })
    return {
      message: response.data.message || 'Password reset email sent'
    }
  }
  async resetPassword(resetData) {
    const response = await this.post('/reset-password', {
      token: resetData.token,
      email: resetData.email.trim().toLowerCase(),
      password: resetData.password
    })
    return {
      message: response.data.message || 'Password reset successfully'
    }
  }
  async verifyEmail(token) {
    const response = await this.post('/verify-email', {
      token: token
    })
    return {
      message: response.data.message || 'Email verified successfully'
    }
  }
  async resendEmailVerification(email) {
    const response = await this.post('/resend-verification', {
      email: email.trim().toLowerCase()
    })
    return {
      message: response.data.message || 'Verification email sent'
    }
  }
  async checkUsernameAvailability(username) {
    const response = await this.get('/check-username', {
      username: username.trim()
    })
    return {
      available: response.data.available,
      suggestions: response.data.suggestions || []
    }
  }
  async checkEmailAvailability(email) {
    const response = await this.get('/check-email', {
      email: email.trim().toLowerCase()
    })
    return {
      available: response.data.available
    }
  }
  async getUserPermissions() {
    const response = await this.get('/permissions')
    return response.data.permissions || []
  }
  async uploadProfilePicture(file, onProgress = null) {
    const response = await this.upload('/profile-picture', file, {}, onProgress)
    return {
      user: response.data.user,
      profilePictureUrl: response.data.profile_picture_url,
      message: response.data.message || 'Profile picture updated'
    }
  }
  async deleteProfilePicture() {
    const response = await this.delete('/profile-picture')
    return {
      user: response.data.user,
      message: response.data.message || 'Profile picture removed'
    }
  }
  async getAccountSettings() {
    const response = await this.get('/settings')
    return response.data.settings || {}
  }
  async updateAccountSettings(settings) {
    const response = await this.patch('/settings', settings)
    return {
      settings: response.data.settings,
      message: response.data.message || 'Settings updated successfully'
    }
  }
  async enableTwoFactor() {
    const response = await this.post('/two-factor/enable')
    return {
      qrCode: response.data.qr_code,
      backupCodes: response.data.backup_codes,
      secret: response.data.secret
    }
  }
  async verifyTwoFactor(code) {
    const response = await this.post('/two-factor/verify', {
      code: code.trim()
    })
    return {
      enabled: response.data.enabled,
      backupCodes: response.data.backup_codes,
      message: response.data.message || 'Two-factor authentication enabled'
    }
  }
  async disableTwoFactor(password) {
    const response = await this.post('/two-factor/disable', {
      password: password
    })
    return {
      message: response.data.message || 'Two-factor authentication disabled'
    }
  }
  async validateTwoFactorLogin(loginToken, code) {
    const response = await this.post('/two-factor/validate', {
      login_token: loginToken,
      code: code.trim()
    })
    return {
      user: response.data.user,
      token: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresIn: response.data.expires_in
    }
  }
  async getActiveSessions() {
    const response = await this.get('/sessions')
    return response.data.sessions || []
  }
  async revokeSession(sessionId) {
    const response = await this.delete(`/sessions/${sessionId}`)
    return {
      message: response.data.message || 'Session revoked successfully'
    }
  }
  async revokeAllOtherSessions() {
    const response = await this.post('/sessions/revoke-all')
    return {
      message: response.data.message || 'All other sessions revoked'
    }
  }
}
const authService = new AuthService()
export default authService
export { AuthService }