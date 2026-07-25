/**
 * Message Service
 *
 * Handles sending messages through WhatsApp.
 * Retrieves the correct client from Session Manager and delivers messages.
 */

const logger = require('../utils/logger');
const { sessionManager, SessionStatus } = require('./session.manager');
const { NotFoundError, ServiceUnavailableError } = require('../utils/errors');
const { formatChatId, sleep, randomDelay } = require('../utils/helpers');

class MessageService {
  /**
   * Send a text message via WhatsApp.
   * @param {string} businessId - The business that owns the WhatsApp session.
   * @param {string} to - Recipient phone number.
   * @param {string} message - Message body to send.
   * @returns {Promise<{status: string, business_id: string, to: string, message_id: string}>}
   */
  async sendMessage(businessId, to, message) {
    // Get the WhatsApp client for this business
    const client = sessionManager.getClient(businessId);

    if (!client) {
      throw new NotFoundError(`No active session found for business: ${businessId}`);
    }

    const status = sessionManager.getStatus(businessId);
    if (status !== SessionStatus.CONNECTED) {
      throw new ServiceUnavailableError(
        `Session for business ${businessId} is not connected (current status: ${status})`
      );
    }

    const chatId = formatChatId(to);

    logger.info(
      `Sending message to [${chatId}] for business [${businessId}]`,
      'MessageService'
    );

    try {
      // Simulate typing indicator
      const chat = await client.getChatById(chatId);
      await chat.sendStateTyping();

      // Human-like delay (2-5 seconds)
      const delay = randomDelay(5000, 8000);
      await sleep(delay);

      // Send the message
      const sentMessage = await client.sendMessage(chatId, message);

      // Clear typing state
      await chat.clearState();

      logger.info(
        `Message sent to [${chatId}] for business [${businessId}]`,
        'MessageService'
      );

      return {
        status: 'success',
        business_id: businessId,
        to,
        message_id: sentMessage.id?._serialized || sentMessage.id?.id || null,
      };
    } catch (error) {
      // Fallback: try sending without chat object (for new conversations)
      logger.warn(
        `Chat object unavailable, attempting direct send to [${chatId}]`,
        'MessageService'
      );

      try {
        const sentMessage = await client.sendMessage(chatId, message);

        return {
          status: 'success',
          business_id: businessId,
          to,
          message_id: null,
        };
      } catch (sendError) {
        logger.error(
          `Failed to send message to [${chatId}] for business [${businessId}]`,
          'MessageService',
          sendError
        );
        throw sendError;
      }
    }
  }
}

module.exports = new MessageService();