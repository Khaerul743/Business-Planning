/**
 * Controllers barrel export
 */

const sessionController = require('./session.controller');
const messageController = require('./message.controller');
const healthController = require('./health.controller');

module.exports = { sessionController, messageController, healthController };
