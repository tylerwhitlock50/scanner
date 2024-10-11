import axios from 'axios';

// Check for the environment variable and default to localhost:5000 if not found
const baseURL = process.env.VITE_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: baseURL,
});

export default api;
