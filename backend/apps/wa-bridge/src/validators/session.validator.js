/**
 * Session Request Validators
 *
 * Validates incoming requests for session-related endpoints.
 */

const { ValidationError } = require('../utils/errors');

/**
 * Validate create session request body.
 * @param {object} body - Request body.
 * @throws {ValidationError} If validation fails.
 */
function validateCreateSession(body) {
  const errors = [];

  if (!body.business_id) {
    errors.push({ field: 'business_id', message: 'business_id is required' });
  } else if (typeof body.business_id !== 'string') {
    errors.push({ field: 'business_id', message: 'business_id must be a string' });
  } else if (body.business_id.trim().length === 0) {
    errors.push({ field: 'business_id', message: 'business_id cannot be empty' });
  }

  if (errors.length > 0) {
    throw new ValidationError('Invalid request body', errors);
  }
}

module.exports = { validateCreateSession };
