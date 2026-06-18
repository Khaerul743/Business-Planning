/**
 * Message Request Validators
 *
 * Validates incoming requests for message-related endpoints.
 */

const { ValidationError } = require('../utils/errors');

/**
 * Validate send message request body.
 * @param {object} body - Request body.
 * @throws {ValidationError} If validation fails.
 */
function validateSendMessage(body) {
  const errors = [];

  if (!body.business_id) {
    errors.push({ field: 'business_id', message: 'business_id is required' });
  } else if (typeof body.business_id !== 'string') {
    errors.push({ field: 'business_id', message: 'business_id must be a string' });
  }

  if (!body.to) {
    errors.push({ field: 'to', message: 'to (phone number) is required' });
  } else if (typeof body.to !== 'string') {
    errors.push({ field: 'to', message: 'to must be a string' });
  }

  if (!body.message) {
    errors.push({ field: 'message', message: 'message is required' });
  } else if (typeof body.message !== 'string') {
    errors.push({ field: 'message', message: 'message must be a string' });
  }

  if (errors.length > 0) {
    throw new ValidationError('Invalid request body', errors);
  }
}

module.exports = { validateSendMessage };
