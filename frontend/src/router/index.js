import { createRouter, createWebHistory } from 'vue-router'
const Login = () => import('../views/auth/Login.vue')
const Register = () => import('../views/auth/Register.vue')
const UserDashboard = () => import('../views/user/Dashboard.vue')
const ReserveParking = () => import('../views/user/ReserveParking.vue')
const MyBookings = () => import('../views/user/MyBookings.vue')
const UserStatistics = () => import('../views/user/Statistics.vue')
const AdminDashboard = () => import('../views/admin/Dashboard.vue')
const ParkingLots = () => import('../views/admin/ParkingLots.vue')
const Users = () => import('../views/admin/Users.vue')
const Home = () => import('../views/Home.vue')
const NotFound = () => import('../views/NotFound.vue')
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Welcome',
      public: true
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: {
      title: 'Login',
      public: true,
      hideForAuth: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: {
      title: 'Register',
      public: true,
      hideForAuth: true
    }
  },
  {
    path: '/user',
    redirect: '/user/dashboard',
    meta: {
      requiresAuth: true,
      userOnly: true
    }
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: {
      title: 'User Dashboard',
      requiresAuth: true,
      userOnly: true
    }
  },
  {
    path: '/user/reserve-parking',
    name: 'ReserveParking',
    component: ReserveParking,
    meta: {
      title: 'Reserve Parking',
      requiresAuth: true,
      userOnly: true
    }
  },
  {
    path: '/user/my-bookings',
    name: 'MyBookings',
    component: MyBookings,
    meta: {
      title: 'My Bookings',
      requiresAuth: true,
      userOnly: true
    }
  },
  {
    path: '/user/statistics',
    name: 'UserStatistics',
    component: UserStatistics,
    meta: {
      title: 'My Statistics',
      requiresAuth: true,
      userOnly: true
    }
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard',
    meta: {
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      title: 'Admin Dashboard',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/parking-lots',
    name: 'ParkingLots',
    component: ParkingLots,
    meta: {
      title: 'Manage Parking Lots',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/admin/users',
    name: 'Users',
    component: Users,
    meta: {
      title: 'Manage Users',
      requiresAuth: true,
      requiresAdmin: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: 'Page Not Found',
      public: true
    }
  }
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})
const isAuthenticated = () => {
  return !!localStorage.getItem('access_token')
}
const isAdmin = () => {
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  return user.is_admin === true
}
const isTokenExpired = () => {
  const token = localStorage.getItem('access_token')
  if (!token) return true
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return Date.now() >= payload.exp * 1000
  } catch {
    return true
  }
}
router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title ?
    `${to.meta.title} - Vehicle Parking App V2` :
    'Vehicle Parking App V2'
  if (to.meta.requiresAuth) {
    if (!isAuthenticated() || isTokenExpired()) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }
    if (to.meta.requiresAdmin && !isAdmin()) {
      next('/user/dashboard')
      return
    }
    if (to.meta.userOnly && isAdmin()) {
      next('/admin/dashboard')
      return
    }
  }
  if (to.meta.hideForAuth && isAuthenticated()) {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    if (user.is_admin) {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
    return
  }
  next()
})
router.afterEach((to, from) => {
  console.log(`Navigated from ${from.path} to ${to.path}`)
  const navbarCollapse = document.querySelector('.navbar-collapse')
  if (navbarCollapse && navbarCollapse.classList.contains('show')) {
    navbarCollapse.classList.remove('show')
  }
})
router.onError((error) => {
  console.error('Router error:', error)
  if (error.message.includes('Loading chunk')) {
    window.location.reload()
  }
})
export default router