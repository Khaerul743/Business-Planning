/**
 * Logger Utility
 *
 * Provides structured logging with timestamps and log levels.
 * Can be replaced with winston/pino in production.
 */

const { env } = require('../config');

const LogLevel = {
  DEBUG: 'DEBUG',
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
};

/**
 * Formats a log message with timestamp, level, and context.
 */
function formatMessage(level, context, message) {
  const timestamp = new Date().toISOString();
  const prefix = context ? `[${context}]` : '';
  return `${timestamp} [${level}] ${prefix} ${message}`;
}

const logger = {
  debug(message, context = '') {
    if (env.isDevelopment) {
      console.debug(formatMessage(LogLevel.DEBUG, context, message));
    }
  },

  info(message, context = '') {
    console.info(formatMessage(LogLevel.INFO, context, message));
  },

  warn(message, context = '') {
    console.warn(formatMessage(LogLevel.WARN, context, message));
  },

  error(message, context = '', error = null) {
    console.error(formatMessage(LogLevel.ERROR, context, message));
    if (error && env.isDevelopment) {
      console.error(error.stack || error);
    }
  },
};

module.exports = logger;
