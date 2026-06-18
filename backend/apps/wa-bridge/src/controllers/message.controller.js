/**
 * Message Controller
 *
 * Handles HTTP requests related to sending messages via WhatsApp.
 */

const messageService = require('../services/message.service');
const { validateSendMessage } = require('../validators/message.validator');

const messageController = {
  /**
   * POST /api/messages/send
   * Send a message through WhatsApp.
   */
  async sendMessage(req, res, next) {
    try {
      validateSendMessage(req.body);

      const { business_id, to, message } = req.body;
      const result = await messageService.sendMessage(business_id, to, message);

      return res.status(200).json({
        success: true,
        data: result,
      });
    } catch (error) {
      next(error);
    }
  },
};

module.exports = messageController;
