// API layer for ML Visualizer backend using Axios
// Makes HTTP requests to FastAPI backend per spec.md §5 contracts.

import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30 second timeout
});

// Optional: Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optional: Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error status
      console.error(`API Error: ${error.response.status}`, error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('API Error: No response received', error.request);
    } else {
      // Error in request setup
      console.error('API Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// ---------- /api/regression ----------
export async function runRegression(req) {
  try {
    const response = await api.post('/regression', req);
    return response.data;
  } catch (error) {
    throw new Error(`Regression API error: ${error.response?.status || error.message}`);
  }
}

// ---------- /api/knn ----------
export async function runKNN(req) {
  try {
    const response = await api.post('/knn', req);
    return response.data;
  } catch (error) {
    throw new Error(`KNN API error: ${error.response?.status || error.message}`);
  }
}

// ---------- /api/decision_tree ----------
export async function runDecisionTree(req) {
  try {
    const response = await api.post('/decision_tree', req);
    return response.data;
  } catch (error) {
    throw new Error(`Decision Tree API error: ${error.response?.status || error.message}`);
  }
}

// ---------- /api/genetic_algorithm ----------
export async function runGA(req) {
  try {
    const response = await api.post('/genetic_algorithm', req);
    return response.data;
  } catch (error) {
    throw new Error(`Genetic Algorithm API error: ${error.response?.status || error.message}`);
  }
}

export default api;
