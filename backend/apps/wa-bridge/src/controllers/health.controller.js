/**
 * Health Controller
 *
 * Provides system health check and status information.
 */

const { sessionManager } = require('../services/session.manager');

const healthController = {
  /**
   * GET /api/health
   * Basic health check.
   */
  async healthCheck(req, res) {
    const sessions = sessionManager.listSessions();

    return res.status(200).json({
      status: 'ok',
      service: 'wa-bridge',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      sessions: {
        total: sessions.length,
        connected: sessions.filter((s) => s.status === 'connected').length,
      },
    });
  },
};

module.exports = healthController;
