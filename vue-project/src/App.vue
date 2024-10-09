<template>
  <div class="app-container">
    <header>
      <img alt="Company Logo" class="logo" src="@/assets/Huxlogo.webp"/>
      <nav>
        <RouterLink to="/">Batch Input</RouterLink>
        <RouterLink to="/scan">OCR Scanning</RouterLink>
        <RouterLink to="/review">Compliance Review</RouterLink>
      </nav>
    </header>

    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* Ensure the div wraps everything and centers it */
.app-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Vertically centers the content inside the div */
  align-items: center; /* Horizontally centers the content */
  min-height: 100vh; /* Ensures the div takes full viewport height */
}

/* Make the header stretch across the whole page */
header {
  width: 100%;
  display: flex;
  justify-content: space-between; /* Space between the logo and nav */
  align-items: center;
  padding: 1rem;
  background-color: #f5f5f5;
  position: sticky; /* Keep the header at the top */
  top: 0;
  z-index: 1000;
}

.logo {
  margin-right: 2rem;
  max-width: 125px;
  display: block;
}

nav {
  display: flex;
  justify-content: flex-end; /* Align links to the right */
  flex-grow: 1;
}

nav a {
  margin-right: 1.5rem;
  text-decoration: none;
  color: #333;
  font-weight: bold;
  white-space: nowrap; /* Prevent links from wrapping */
}

nav a.router-link-exact-active {
  color: #42b983;
}

main {
  padding: 2rem;
  max-width: 900px; /* Control max-width for readability */
  margin: 0 auto; /* Center the main content */
}

@media (max-width: 768px) {
  header {
    flex-direction: column;
    align-items: center;
  }

  nav {
    justify-content: center; /* Center the navigation links on mobile */
    margin-top: 1rem;
  }

  nav a {
    margin-right: 1rem;
  }
}
</style>
