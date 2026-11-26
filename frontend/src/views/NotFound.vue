<template>
  <div class="not-found">
    <div class="container text-center">
      <div class="error-content">
        <h1 class="error-code">404</h1>
        <h2 class="error-title">Page Not Found</h2>
        <p class="error-message">The page you're looking for doesn't exist.</p>
        <router-link to="/" class="btn btn-primary">
          <i class="fas fa-home me-2"></i>Go Home
        </router-link>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: 'NotFoundPage'
}
</script>
<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #000133, #4B006E);
  color: white;
}
.error-code {
  font-size: 8rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: #8AB8FE;
}
.error-title {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.error-message {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}
.btn-primary {
  background: linear-gradient(135deg, #8AB8FE, #4B006E);
  border: none;
  border-radius: 8px;
  font-weight: 600;
  padding: 1rem 2rem;
}
</style>