import './assets/main.css';

import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';

// Import Bootstrap styles
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';


// Import Vuetify from the plugins folder
import vuetify from './plugins/vuetify';
import keycloak from './services/keycloak';


keycloak.init({ onLoad: 'login-required' }).then((authenticated) => {
    if (!authenticated) {
      window.location.reload();
    } else {
      const app = createApp(App);
      app.config.globalProperties.$keycloak = keycloak;
      app.mount('#app');
    }
  }).catch(() => {
    console.error('Keycloak initialization failed');
  });

// Create the app instance
const app = createApp(App);

// Use Vuetify, Pinia, and the router
app.use(vuetify);  // Make sure Vuetify is used
app.use(createPinia());
app.use(router);

// Mount the app
app.mount('#app');
