<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header>
    <img alt="Company Logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <nav>
      <RouterLink to="/">Batch Input</RouterLink>
      <RouterLink to="/scan">OCR Scanning</RouterLink>
      <RouterLink to="/review">Compliance Review</RouterLink>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>

<style scoped>
header {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: #f5f5f5;
}

.logo {
  margin-right: 2rem;
}

nav {
  flex-grow: 1;
}

nav a {
  margin-right: 1rem;
  text-decoration: none;
  color: #333;
  font-weight: bold;
}

nav a.router-link-exact-active {
  color: #42b983;
}

main {
  padding: 2rem;
}
</style>
