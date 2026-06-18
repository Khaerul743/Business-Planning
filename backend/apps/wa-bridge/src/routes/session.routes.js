/**
 * Session Routes
 *
 * Defines routes for WhatsApp session management.
 *
 * Routes:
 *   POST   /api/sessions                       - Create a new session
 *   GET    /api/sessions                        - List all sessions
 *   GET    /api/sessions/:business_id           - Get session status
 *   DELETE /api/sessions/:business_id           - Destroy a session
 *   POST   /api/sessions/:business_id/reconnect - Reconnect a session
 */

const { Router } = require('express');
const { sessionController } = require('../controllers');

const router = Router();

router.post('/', sessionController.createSession);
router.get('/', sessionController.listSessions);
router.get('/:business_id', sessionController.getSession);
router.delete('/:business_id', sessionController.destroySession);
router.post('/:business_id/reconnect', sessionController.reconnectSession);

module.exports = router;
