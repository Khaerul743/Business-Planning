/**
 * WhatsApp Service
 *
 * Handles creation and lifecycle management of WhatsApp client instances.
 * Acts as a bridge between controllers and the Session Manager.
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const { env } = require('../config');
const logger = require('../utils/logger');
const { sessionManager, SessionStatus } = require('./session.manager');
const { registerClientEvents } = require('../events');
const { ConflictError, NotFoundError } = require('../utils/errors');

class WhatsAppService {
  /**
   * Create a new WhatsApp session for a business.
   * @param {string} businessId
   * @returns {Promise<{business_id: string, session_id: string, status: string, qr_code: string|null}>}
   */
  async createSession(businessId) {
    // Check if session already exists and is active
    if (sessionManager.hasSession(businessId)) {
      const currentStatus = sessionManager.getStatus(businessId);
      if (currentStatus === SessionStatus.CONNECTED) {
        throw new ConflictError(
          `Session for business ${businessId} is already connected`
        );
      }

      // If session exists but disconnected/pending, destroy and recreate
      if (currentStatus !== SessionStatus.DESTROYED) {
        logger.info(
          `Recreating session for ${businessId} (previous status: ${currentStatus})`,
          'WhatsAppService'
        );
        await sessionManager.destroy(businessId);
      }
    }

    logger.info(`Creating new WhatsApp session: ${businessId}`, 'WhatsAppService');

    // Create new whatsapp-web.js client
    const client = new Client({
      authStrategy: new LocalAuth({
        clientId: businessId,
        dataPath: env.sessionPath,
      }),
      puppeteer: {
        headless: true,
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-accelerated-2d-canvas',
          '--no-first-run',
          '--disable-gpu',
        ],
      },
    });

    // Register in session manager
    sessionManager.register(businessId, client);

    // Attach all event handlers
    registerClientEvents(client, businessId);

    // Initialize client (async, will trigger QR event)
    client.initialize().catch((error) => {
      logger.error(`Failed to initialize client: ${businessId}`, 'WhatsAppService', error);
      sessionManager.setStatus(businessId, SessionStatus.DISCONNECTED);
    });

    // Return immediately without waiting for QR code
    return {
      business_id: businessId,
      session_id: businessId,
      status: 'creating',
    };
  }

  /**
   * Get session status and info for a business.
   * @param {string} businessId
   * @returns {{business_id: string, session_id: string, status: string, metadata: object|null, qr_code: string|null}}
   */
  getSessionStatus(businessId) {
    const status = sessionManager.getStatus(businessId);

    if (!status) {
      throw new NotFoundError(`No session found for business: ${businessId}`);
    }

    return {
      business_id: businessId,
      session_id: businessId,
      status,
      metadata: sessionManager.getMetadata(businessId) || null,
      qr_code: status === SessionStatus.PENDING_QR
        ? sessionManager.getQrCode(businessId)
        : null,
    };
  }

  /**
   * List all sessions.
   * @returns {Array}
   */
  listSessions() {
    return sessionManager.listSessions();
  }

  /**
   * Destroy a session.
   * @param {string} businessId
   */
  async destroySession(businessId) {
    if (!sessionManager.hasSession(businessId)) {
      throw new NotFoundError(`No session found for business: ${businessId}`);
    }

    await sessionManager.destroy(businessId);
    return { business_id: businessId, status: SessionStatus.DESTROYED };
  }

  /**
   * Reconnect a disconnected session.
   * @param {string} businessId
   */
  async reconnectSession(businessId) {
    const status = sessionManager.getStatus(businessId);

    if (!status) {
      throw new NotFoundError(`No session found for business: ${businessId}`);
    }

    if (status === SessionStatus.CONNECTED) {
      return { business_id: businessId, status: SessionStatus.CONNECTED, message: 'Already connected' };
    }

    // Destroy and recreate
    await sessionManager.destroy(businessId);
    return this.createSession(businessId);
  }
}

module.exports = new WhatsAppService();
