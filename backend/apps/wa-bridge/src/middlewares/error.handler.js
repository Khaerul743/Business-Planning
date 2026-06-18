/**
 * Global Error Handler Middleware
 *
 * Catches all errors passed via next(error) and returns
 * a consistent JSON error response.
 */

const logger = require('../utils/logger');
const { AppError } = require('../utils/errors');

/**
 * Global error handling middleware.
 * Must have 4 parameters to be recognized by Express as an error handler.
 */
function errorHandler(err, req, res, _next) {
  // Determine if this is an operational (known) error
  if (err instanceof AppError) {
    logger.warn(
      `${err.code} - ${err.message}`,
      'ErrorHandler'
    );

    return res.status(err.statusCode).json({
      success: false,
      error: {
        code: err.code,
        message: err.message,
        details: err.details || undefined,
      },
    });
  }

  // Unknown / unexpected errors
  logger.error(`Unhandled error: ${err.message}`, 'ErrorHandler', err);

  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
    },
  });
}

module.exports = errorHandler;
