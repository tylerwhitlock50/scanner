<template>
  <div class="app-container">
    <nav class="navbar navbar-expand-lg navbar-light bg-light w-100">
      <a class="navbar-brand" href="#">
        <img alt="Company Logo" class="logo" src="@/assets/Huxlogo.webp"/>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink class="nav-link" to="/">Batch Info</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/scan">OCR-Scan</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" to="/review">Review</RouterLink>
          </li>
        </ul>
      </div>
    </nav>

    <main class="mt-1">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
}

.navbar {
  width: 100%;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo {
  max-width: 125px;
}

.navbar-nav {
  flex-direction: row;
}

.nav-link {
  color: #f5f5f5;
  font-weight: bold;
  margin-right: 1rem;
}

.nav-link.router-link-exact-active {
  color: #42b983;
}

.navbar-light .navbar-brand, .navbar-light .nav-link {
  color: #333 !important; /* Darker text for readability on the light background */
  font-weight: bold;
}

.navbar-light .nav-link.router-link-exact-active {
  color: #42b983 !important; /* Highlight color for the active link */
}

main {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .navbar-nav {
    flex-direction: column;
    align-items: center;
  }

  .nav-link {
    margin: 0.5rem 0;
  }
}
</style>
