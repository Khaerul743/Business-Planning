/**
 * Validators barrel export
 */

const { validateCreateSession } = require('./session.validator');
const { validateSendMessage } = require('./message.validator');

module.exports = { validateCreateSession, validateSendMessage };
