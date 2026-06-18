/**
 * Request Logger Middleware
 *
 * Logs incoming HTTP requests with method, URL, and response time.
 */

const logger = require('../utils/logger');

function requestLogger(req, res, next) {
  const start = Date.now();

  // Log when response finishes
  res.on('finish', () => {
    const duration = Date.now() - start;
    const logMessage = `${req.method} ${req.originalUrl} → ${res.statusCode} (${duration}ms)`;

    if (res.statusCode >= 400) {
      logger.warn(logMessage, 'HTTP');
    } else {
      logger.info(logMessage, 'HTTP');
    }
  });

  next();
}

module.exports = requestLogger;
