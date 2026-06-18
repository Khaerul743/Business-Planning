/**
 * Environment Configuration
 *
 * Loads and validates environment variables.
 * Single source of truth for all configuration values.
 */

require('dotenv').config();

const env = {
  port: parseInt(process.env.PORT, 10) || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',
  fastApiUrl: process.env.FASTAPI_URL || 'http://localhost:8000',
  sessionPath: process.env.SESSION_PATH || '.wwebjs_auth',

  get isDevelopment() {
    return this.nodeEnv === 'development';
  },

  get isProduction() {
    return this.nodeEnv === 'production';
  },
};

// Validate required configuration
const requiredVars = ['FASTAPI_URL'];
for (const varName of requiredVars) {
  if (!process.env[varName]) {
    console.warn(`[WARN] Environment variable ${varName} is not set. Using default.`);
  }
}

module.exports = env;
