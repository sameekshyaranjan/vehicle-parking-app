<template>
  <div class="home-page">
    <section class="hero-section">
      <div class="hero-background"></div>
      <div class="container">
        <div class="row align-items-center min-vh-100">
          <div class="col-lg-6">
            <div class="hero-content">
              <div class="hero-badge mb-3">
                <i class="fas fa-star me-2"></i>
                Trusted by Users
              </div>
              <h1 class="hero-title">
                Smart Parking Solutions for
                <span class="text-gradient">Modern Cities</span>
              </h1>
              <p class="hero-description">
                Find, reserve, and manage parking spots effortlessly with our advanced
                vehicle parking management system. Save time, reduce stress, and park smart.
              </p>
              <div class="hero-actions mt-4">
                <router-link
                  v-if="!authStore.isAuthenticated"
                  to="/register"
                  class="btn btn-primary btn-lg me-3"
                >
                  <i class="fas fa-rocket me-2"></i>Get Started Free
                </router-link>
                <router-link
                  v-else
                  :to="authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'"
                  class="btn btn-primary btn-lg me-3"
                >
                  <i class="fas fa-tachometer-alt me-2"></i>Go to Dashboard
                </router-link>
                <button class="btn btn-outline-light btn-lg" @click="scrollToFeatures">
                  <i class="fas fa-play me-2"></i>Learn More
                </button>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-visual">
              <div class="parking-mockup">
                <div class="mockup-container">
                  <div class="phone-mockup">
                    <div class="phone-screen">
                      <div class="app-header">
                        <i class="fas fa-car"></i>
                        <span>ParkSmart</span>
                      </div>
                      <div class="app-content">
                        <div class="search-bar">
                          <i class="fas fa-search"></i>
                          <span>Find parking near you...</span>
                        </div>
                        <div class="parking-grid">
                          <div class="parking-spot available"></div>
                          <div class="parking-spot occupied"></div>
                          <div class="parking-spot available"></div>
                          <div class="parking-spot available"></div>
                          <div class="parking-spot occupied"></div>
                          <div class="parking-spot available"></div>
                        </div>
                        <div class="booking-button">
                          <span>Reserve Spot</span>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="floating-element location-card">
                    <i class="fas fa-map-marker-alt"></i>
                    <div>
                      <strong>Central Mall</strong>
                      <small>₹50/hour</small>
                    </div>
                  </div>
                  <div class="floating-element booking-card">
                    <i class="fas fa-check-circle"></i>
                    <div>
                      <strong>Booking Confirmed</strong>
                      <small>Spot #A15</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section id="features" class="features-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">Why Choose ParkSmart?</h2>
          <p class="section-description">
            Experience the future of parking with our comprehensive suite of features
          </p>
        </div>
        <div class="row">
          <div class="col-lg-4 col-md-6 mb-4" v-for="feature in features" :key="feature.id">
            <div class="feature-card">
              <div class="feature-icon" :class="feature.iconClass">
                <i class="fas" :class="feature.icon"></i>
              </div>
              <h5 class="feature-title">{{ feature.title }}</h5>
              <p class="feature-description">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    <section class="how-it-works-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="section-title">How It Works</h2>
          <p class="section-description">
            Get started in just three simple steps
          </p>
        </div>
        <div class="row">
          <div class="col-lg-4 mb-4" v-for="(step, index) in steps" :key="step.id">
            <div class="step-card">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-icon">
                <i class="fas" :class="step.icon"></i>
              </div>
              <h5 class="step-title">{{ step.title }}</h5>
              <p class="step-description">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="cta-section py-5">
      <div class="container">
        <div class="cta-container">
          <div class="row align-items-center">
            <div class="col-lg-8">
              <h2 class="cta-title">Ready to Transform Your Parking Experience?</h2>
              <p class="cta-description">
                Join thousands of users who have already made the smart choice.
                Start parking smarter today!
              </p>
            </div>
            <div class="col-lg-4 text-center">
              <router-link
                v-if="!authStore.isAuthenticated"
                to="/register"
                class="btn btn-primary btn-lg"
              >
                <i class="fas fa-rocket me-2"></i>Get Started Now
              </router-link>
              <router-link
                v-else
                :to="authStore.isAdmin ? '/admin/dashboard' : '/user/dashboard'"
                class="btn btn-primary btn-lg"
              >
                <i class="fas fa-tachometer-alt me-2"></i>Go to Dashboard
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '../store/modules/auth'
import { useAdminStore } from '../store/modules/admin'
export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const adminStore = useAdminStore()
    const animatedStats = reactive({
      parkingLots: 0,
      totalSpots: 0,
      users: 0,
      activeBookings: 0
    })
    const features = ref([
      {
        id: 1,
        icon: 'fa-search',
        iconClass: 'bg-primary',
        title: 'Smart Search',
        description: 'Find available parking spots near your destination with real-time availability updates.'
      },
      {
        id: 2,
        icon: 'fa-mobile-alt',
        iconClass: 'bg-success',
        title: 'Mobile First',
        description: 'Book and manage your parking reservations on-the-go with our responsive mobile interface.'
      },
      {
        id: 5,
        icon: 'fa-chart-line',
        iconClass: 'bg-danger',
        title: 'Analytics',
        description: 'Track your parking patterns and expenses with detailed analytics and reports.'
      }
    ])
    const steps = ref([
      {
        id: 1,
        icon: 'fa-search',
        title: 'Search & Discover',
        description: 'Find available parking spots near your destination using our smart search feature.'
      },
      {
        id: 2,
        icon: 'fa-calendar-check',
        title: 'Book & Reserve',
        description: 'Select your preferred spot and book it instantly with flexible timing options.'
      },
      {
        id: 3,
        icon: 'fa-car',
        title: 'Park & Enjoy',
        description: 'Navigate to your reserved spot and enjoy hassle-free parking with peace of mind.'
      }
    ])
    const testimonials = ref([
      {
        id: 1,
        text: 'ParkSmart has completely changed how I think about parking in the city. No more circling around looking for spots!',
        author: 'Rajesh Kumar',
        role: 'Business Professional'
      },
      {
        id: 2,
        text: 'The mobile app is so intuitive and the booking process is seamless. Highly recommended for daily commuters.',
        author: 'Priya Sharma',
        role: 'Software Engineer'
      },
      {
        id: 3,
        text: 'As a business owner, the analytics feature helps me understand my customers\' parking patterns better.',
        author: 'Amit Patel',
        role: 'Restaurant Owner'
      }
    ])
    const scrollToFeatures = () => {
      const featuresElement = document.getElementById('features')
      if (featuresElement) {
        featuresElement.scrollIntoView({ behavior: 'smooth' })
      }
    }
    const animateCounters = () => {
      const targets = {
        parkingLots: adminStore.dashboard.totalLots || 0,
        totalSpots: adminStore.dashboard.totalSpots || 0,
        users: adminStore.dashboard.totalUsers || 0,
        activeBookings: adminStore.dashboard.activeBookings || 0
      }
      const duration = 2000
      const steps = 60
      const stepDuration = duration / steps
      Object.keys(targets).forEach(key => {
        const target = targets[key]
        const increment = target / steps
        let current = 0
        const timer = setInterval(() => {
          current += increment
          if (current >= target) {
            animatedStats[key] = target
            clearInterval(timer)
          } else {
            animatedStats[key] = Math.floor(current)
          }
        }, stepDuration)
      })
    }
    const handleScroll = () => {
      const statsSection = document.querySelector('.live-stats-section')
      if (statsSection) {
        const rect = statsSection.getBoundingClientRect()
        const isVisible = rect.top < window.innerHeight && rect.bottom > 0
        if (isVisible && animatedStats.parkingLots === 0) {
          animateCounters()
        }
      }
    }
    onMounted(async () => {
      window.addEventListener('scroll', handleScroll)
      if (authStore.isAdmin) {
        await adminStore.fetchDashboard()
      }
      setTimeout(handleScroll, 100)
    })
    onUnmounted(() => {
      window.removeEventListener('scroll', handleScroll)
    })
    return {
      authStore,
      adminStore,
      animatedStats,
      features,
      steps,
      testimonials,
      scrollToFeatures
    }
  }
}
</script>
<style scoped>
.home-page {
  overflow-x: hidden;
}
.hero-section {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  overflow: hidden;
}
.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image:
    radial-gradient(circle at 20% 20%, rgba(138, 184, 254, 0.1) 2px, transparent 2px),
    radial-gradient(circle at 80% 40%, rgba(138, 184, 254, 0.1) 2px, transparent 2px),
    radial-gradient(circle at 40% 80%, rgba(138, 184, 254, 0.1) 2px, transparent 2px);
  background-size: 100px 100px;
  animation: float 20s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}
.hero-content {
  position: relative;
  z-index: 2;
}
.hero-badge {
  display: inline-block;
  background: rgba(138, 184, 254, 0.2);
  color: var(--text-accent);
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 600;
}
.hero-title {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}
.text-gradient {
  background: linear-gradient(135deg, var(--text-accent), #ffffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-description {
  font-size: 1.25rem;
  line-height: 1.6;
  opacity: 0.9;
  margin-bottom: 2rem;
}
.btn-primary {
  background: linear-gradient(135deg, var(--text-accent), var(--secondary-color));
  border: none;
  border-radius: 50px;
  padding: 1rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(138, 184, 254, 0.4);
}
.btn-outline-light {
  border: 2px solid var(--text-accent);
  color: var(--text-accent);
  border-radius: 50px;
  padding: 1rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
}
.btn-outline-light:hover {
  background-color: var(--text-accent);
  border-color: var(--text-accent);
  color: var(--primary-color);
}
.hero-stats {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(138, 184, 254, 0.3);
}
.stat-item {
  text-align: center;
}
.stat-item h4 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-accent);
  margin-bottom: 0.5rem;
}
.stat-item small {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}
.hero-visual {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.mockup-container {
  position: relative;
}
.phone-mockup {
  width: 280px;
  height: 560px;
  background: #000;
  border-radius: 30px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}
.phone-screen {
  width: 100%;
  height: 100%;
  background: white;
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
}
.app-header {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--primary-color);
  font-weight: 700;
  font-size: 1.2rem;
  margin-bottom: 20px;
}
.search-bar {
  background: #f8f9fa;
  padding: 12px 16px;
  border-radius: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #6c757d;
  margin-bottom: 20px;
}
.parking-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}
.parking-spot {
  aspect-ratio: 1;
  border-radius: 8px;
}
.parking-spot.available {
  background: #d4edda;
  border: 2px solid #28a745;
}
.parking-spot.occupied {
  background: #f8d7da;
  border: 2px solid #dc3545;
}
.booking-button {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: white;
  padding: 15px;
  border-radius: 25px;
  text-align: center;
  font-weight: 600;
  margin-top: auto;
}
.floating-element {
  position: absolute;
  background: white;
  padding: 12px 16px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--primary-color);
  font-size: 0.9rem;
  animation: floating 3s ease-in-out infinite;
}
.location-card {
  top: 20%;
  left: -20%;
  animation-delay: 0s;
}
.booking-card {
  bottom: 30%;
  right: -20%;
  animation-delay: 1.5s;
}
@keyframes floating {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
}
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--primary-color);
  margin-bottom: 1rem;
}
.section-description {
  font-size: 1.1rem;
  color: #6c757d;
  max-width: 600px;
  margin: 0 auto;
}
.features-section {
  background: #f8f9fa;
}
.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  transition: all 0.3s ease;
  height: 100%;
}
.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 30px rgba(0, 1, 51, 0.15);
}
.feature-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  color: white;
  margin: 0 auto 1.5rem;
}
.feature-icon.bg-primary {
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
}
.feature-title {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 1rem;
}
.feature-description {
  color: #6c757d;
  line-height: 1.6;
}
.how-it-works-section {
  background: white;
}
.step-card {
  text-align: center;
  position: relative;
  padding: 2rem 1rem;
}
.step-number {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
}
.step-icon {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(138, 184, 254, 0.1), rgba(255, 255, 255, 0.9));
  border: 3px solid var(--text-accent);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: var(--secondary-color);
  margin: 2rem auto 1.5rem;
}
.step-title {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 1rem;
}
.step-description {
  color: #6c757d;
  line-height: 1.6;
}
.live-stats-section {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}
.stats-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 3rem 2rem;
  backdrop-filter: blur(10px);
}
.live-stat {
  padding: 1rem;
}
.live-stat .stat-icon {
  font-size: 3rem;
  color: var(--text-accent);
  margin-bottom: 1rem;
}
.stat-number {
  font-size: 3rem;
  font-weight: 800;
  color: white;
  margin-bottom: 0.5rem;
}
.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
}
.testimonials-section {
  background: #f8f9fa;
}
.testimonial-card {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 1, 51, 0.1);
  height: 100%;
  display: flex;
  flex-direction: column;
}
.testimonial-content {
  flex: 1;
}
.stars {
  color: #ffc107;
}
.testimonial-text {
  font-style: italic;
  color: #6c757d;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}
.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}
.author-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}
.author-name {
  font-weight: 600;
  color: var(--primary-color);
  margin-bottom: 0.25rem;
}
.author-role {
  color: #6c757d;
}
.cta-section {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
}
.cta-container {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 3rem 2rem;
  backdrop-filter: blur(10px);
}
.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}
.cta-description {
  font-size: 1.1rem;
  opacity: 0.9;
  line-height: 1.6;
}
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  .hero-description {
    font-size: 1.1rem;
  }
  .phone-mockup {
    width: 240px;
    height: 480px;
  }
  .floating-element {
    display: none;
  }
  .section-title {
    font-size: 2rem;
  }
  .feature-icon,
  .step-icon {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  .stat-number {
    font-size: 2.5rem;
  }
  .cta-title {
    font-size: 2rem;
  }
}
@media (max-width: 576px) {
  .hero-title {
    font-size: 2rem;
  }
  .btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
  }
  .stats-container,
  .cta-container {
    padding: 2rem 1rem;
  }
}
</style>