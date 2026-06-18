/**
 * Session Controller
 *
 * Handles HTTP requests related to WhatsApp session management.
 */

const whatsappService = require('../services/whatsapp.service');
const { validateCreateSession } = require('../validators/session.validator');

const sessionController = {
  /**
   * POST /api/sessions
   * Create a new WhatsApp session.
   */
  async createSession(req, res, next) {
    try {
      validateCreateSession(req.body);

      const { business_id } = req.body;
      const result = await whatsappService.createSession(business_id);

      return res.status(201).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * GET /api/sessions/:business_id
   * Get session status for a specific business.
   */
  async getSession(req, res, next) {
    try {
      const { business_id } = req.params;
      const result = whatsappService.getSessionStatus(business_id);

      return res.status(200).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * GET /api/sessions
   * List all active sessions.
   */
  async listSessions(req, res, next) {
    try {
      const sessions = whatsappService.listSessions();

      return res.status(200).json({
        success: true,
        data: sessions,
        total: sessions.length,
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * DELETE /api/sessions/:business_id
   * Destroy a WhatsApp session.
   */
  async destroySession(req, res, next) {
    try {
      const { business_id } = req.params;
      const result = await whatsappService.destroySession(business_id);

      return res.status(200).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * POST /api/sessions/:business_id/reconnect
   * Reconnect a disconnected session.
   */
  async reconnectSession(req, res, next) {
    try {
      const { business_id } = req.params;
      const result = await whatsappService.reconnectSession(business_id);

      return res.status(200).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  },
};

module.exports = sessionController;
