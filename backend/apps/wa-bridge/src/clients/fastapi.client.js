/**
 * FastAPI Client
 *
 * Axios-based HTTP client for communicating with the FastAPI backend.
 * Centralized request/response handling and error logging.
 */

const axios = require('axios');
const { env } = require('../config');
const logger = require('../utils/logger');

const fastApiClient = axios.create({
  baseURL: env.fastApiUrl,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
fastApiClient.interceptors.request.use(
  (config) => {
    logger.debug(
      `→ ${config.method.toUpperCase()} ${config.baseURL}${config.url}`,
      'FastAPI'
    );
    return config;
  },
  (error) => {
    logger.error('Request interceptor error', 'FastAPI', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
fastApiClient.interceptors.response.use(
  (response) => {
    logger.debug(
      `← ${response.status} ${response.config.method.toUpperCase()} ${response.config.url}`,
      'FastAPI'
    );
    return response;
  },
  (error) => {
    if (error.response) {
      logger.error(
        `← ${error.response.status} ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${JSON.stringify(error.response.data)}`,
        'FastAPI'
      );
    } else if (error.request) {
      logger.error(
        `No response received for ${error.config?.method?.toUpperCase()} ${error.config?.url}`,
        'FastAPI'
      );
    } else {
      logger.error(`Request setup error: ${error.message}`, 'FastAPI');
    }
    return Promise.reject(error);
  }
);

module.exports = fastApiClient;
