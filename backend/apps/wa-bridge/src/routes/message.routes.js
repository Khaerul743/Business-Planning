/**
 * Message Routes
 *
 * Defines routes for sending messages through WhatsApp.
 *
 * Routes:
 *   POST /api/messages/send - Send a message via WhatsApp
 */

const { Router } = require('express');
const { messageController } = require('../controllers');

const router = Router();

router.post('/send', messageController.sendMessage);

module.exports = router;
