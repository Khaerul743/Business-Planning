/**
 * FastAPI Event Service
 *
 * Handles sending WhatsApp session events to the FastAPI backend.
 */

const { fastApiClient } = require('../clients');
const logger = require('../utils/logger');

class FastApiEventService {
  /**
   * Send an event payload to the FastAPI event endpoint.
   * @param {object} payload 
   */
  async sendEvent(payload) {
    try {
      await fastApiClient.post('/api/whatsapp/event', payload);
      logger.debug(`Event '${payload.event}' sent to FastAPI for business: ${payload.business_id}`, 'FastApiEventService');
    } catch (error) {
      logger.error(`Failed to send event '${payload.event}' to FastAPI for business: ${payload.business_id}`, 'FastApiEventService', error);
    }
  }

  async sendQrEvent(businessId, qr) {
    const payload = {
      event: 'qr',
      business_id: businessId,
      session_id: businessId,
      status: 'pending_qr',
      qr_code: qr,
    };
    await this.sendEvent(payload);
  }

  async sendAuthenticatingEvent(businessId) {
    const payload = {
      event: 'authenticating',
      business_id: businessId,
      session_id: businessId,
      status: 'authenticating',
    };
    await this.sendEvent(payload);
  }

  async sendReadyEvent(businessId, phoneNumber, displayName) {
    const payload = {
      event: 'ready',
      business_id: businessId,
      session_id: businessId,
      status: 'connected',
      phone_number: phoneNumber,
      display_name: displayName,
    };
    await this.sendEvent(payload);
  }

  async sendDisconnectedEvent(businessId, reason) {
    const payload = {
      event: 'disconnected',
      business_id: businessId,
      session_id: businessId,
      status: 'disconnected',
      reason: reason,
    };
    await this.sendEvent(payload);
  }

  async sendAuthFailureEvent(businessId, message) {
    const payload = {
      event: 'auth_failure',
      business_id: businessId,
      session_id: businessId,
      status: 'auth_failure',
      message: message,
    };
    await this.sendEvent(payload);
  }
  async sendWebhook(payload) {
    try {
      await fastApiClient.post('/api/whatsapp/webhook', payload);
      logger.debug(`Webhook message sent to FastAPI`, 'FastApiEventService');
    } catch (error) {
      logger.error(`Failed to send webhook message to FastAPI`, 'FastApiEventService', error);
    }
  }
}

module.exports = new FastApiEventService();
