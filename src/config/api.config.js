/**
 * API Configuration
 * Centralized configuration for backend API endpoints
 */

// Backend API URL - update this for production deployment
export const API_CONFIG = {
  // Base URL for all API calls
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  
  // API endpoints
  endpoints: {
    detect: "/detect",
    analyzeLLM: "/analyze-llm",
  },
  
  // Request timeout in milliseconds
  timeout: 30000,
  
  // Default headers
  headers: {
    "Content-Type": "application/json",
  }
};

/**
 * Get full endpoint URL
 */
export function getEndpointURL(endpoint) {
  return `${API_CONFIG.baseURL}${API_CONFIG.endpoints[endpoint] || endpoint}`;
}

/**
 * Create request options
 */
export function createRequestOptions(method, body = null) {
  const options = {
    method,
    headers: { ...API_CONFIG.headers },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  return options;
}
