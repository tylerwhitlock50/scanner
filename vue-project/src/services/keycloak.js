import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  // Use the internal Docker network URL for backend communication
  url: window.location.hostname.includes('localhost') 
    ? 'http://localhost:8081'   // Access from the host (for development)
    : 'http://keycloak_auth:8080',  // Access from inside Docker network
  realm: 'your-realm',   // Replace with your realm name
  clientId: 'vue-client',  // Replace with your client ID
});

export default keycloak;
