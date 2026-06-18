/**
 * Health Routes
 *
 * Routes:
 *   GET /api/health - Service health check
 */

const { Router } = require('express');
const { healthController } = require('../controllers');

const router = Router();

router.get('/', healthController.healthCheck);

module.exports = router;
