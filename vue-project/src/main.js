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

// Create the app instance
const app = createApp(App);

// Use Vuetify, Pinia, and the router
app.use(vuetify);  // Make sure Vuetify is used
app.use(createPinia());
app.use(router);

// Mount the app
app.mount('#app');
