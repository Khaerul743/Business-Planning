/**
 * Routes Index
 *
 * Aggregates all route modules and mounts them under /api.
 */

const { Router } = require('express');
const sessionRoutes = require('./session.routes');
const messageRoutes = require('./message.routes');
const healthRoutes = require('./health.routes');

const router = Router();

router.use('/sessions', sessionRoutes);
router.use('/messages', messageRoutes);
router.use('/health', healthRoutes);

module.exports = router;
