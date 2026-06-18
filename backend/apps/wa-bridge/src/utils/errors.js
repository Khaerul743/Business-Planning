/**
 * Custom Application Errors
 *
 * Provides typed errors for consistent error handling throughout the application.
 */

class AppError extends Error {
  /**
   * @param {string} message - Error message.
   * @param {number} statusCode - HTTP status code.
   * @param {string} code - Application-specific error code.
   */
  constructor(message, statusCode = 500, code = 'INTERNAL_ERROR') {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = statusCode;
    this.code = code;
    Error.captureStackTrace(this, this.constructor);
  }
}

class NotFoundError extends AppError {
  constructor(message = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

class ValidationError extends AppError {
  constructor(message = 'Validation failed', details = []) {
    super(message, 400, 'VALIDATION_ERROR');
    this.details = details;
  }
}

class ConflictError extends AppError {
  constructor(message = 'Resource already exists') {
    super(message, 409, 'CONFLICT');
  }
}

class ServiceUnavailableError extends AppError {
  constructor(message = 'Service unavailable') {
    super(message, 503, 'SERVICE_UNAVAILABLE');
  }
}

module.exports = {
  AppError,
  NotFoundError,
  ValidationError,
  ConflictError,
  ServiceUnavailableError,
};
