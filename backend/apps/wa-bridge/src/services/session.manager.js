/**
 * Session Manager Service (Singleton)
 *
 * Manages all WhatsApp client instances across multiple tenants.
 * Responsibilities:
 *   - Register new WhatsApp client instances
 *   - Retrieve client by business_id
 *   - Remove / destroy client sessions
 *   - List all active sessions
 *   - Track session status per business
 */

const logger = require('../utils/logger');

/**
 * Session statuses
 */
const SessionStatus = {
  PENDING_QR: 'pending_qr',
  AUTHENTICATING: 'authenticating',
  CONNECTED: 'connected',
  DISCONNECTED: 'disconnected',
  DESTROYED: 'destroyed',
};

class SessionManager {
  constructor() {
    if (SessionManager._instance) {
      return SessionManager._instance;
    }

    /** @type {Map<string, import('whatsapp-web.js').Client>} */
    this._clients = new Map();

    /** @type {Map<string, string>} */
    this._statuses = new Map();

    /** @type {Map<string, object>} */
    this._metadata = new Map();

    /** @type {Map<string, string>} */
    this._qrCodes = new Map();

    SessionManager._instance = this;
  }

  /**
   * Register a new client instance.
   * @param {string} businessId
   * @param {import('whatsapp-web.js').Client} client
   */
  register(businessId, client) {
    this._clients.set(businessId, client);
    this._statuses.set(businessId, SessionStatus.PENDING_QR);
    logger.info(`Session registered: ${businessId}`, 'SessionManager');
  }

  /**
   * Get client by business_id.
   * @param {string} businessId
   * @returns {import('whatsapp-web.js').Client | undefined}
   */
  getClient(businessId) {
    return this._clients.get(businessId);
  }

  /**
   * Check if a session exists.
   * @param {string} businessId
   * @returns {boolean}
   */
  hasSession(businessId) {
    return this._clients.has(businessId);
  }

  /**
   * Get session status.
   * @param {string} businessId
   * @returns {string | undefined}
   */
  getStatus(businessId) {
    return this._statuses.get(businessId);
  }

  /**
   * Update session status.
   * @param {string} businessId
   * @param {string} status
   */
  setStatus(businessId, status) {
    this._statuses.set(businessId, status);
    logger.info(`Session status updated: ${businessId} → ${status}`, 'SessionManager');
  }

  /**
   * Store QR code for a session.
   * @param {string} businessId
   * @param {string} qrCode
   */
  setQrCode(businessId, qrCode) {
    this._qrCodes.set(businessId, qrCode);
  }

  /**
   * Get stored QR code.
   * @param {string} businessId
   * @returns {string | undefined}
   */
  getQrCode(businessId) {
    return this._qrCodes.get(businessId);
  }

  /**
   * Store session metadata (phone number, display name, etc.).
   * @param {string} businessId
   * @param {object} metadata
   */
  setMetadata(businessId, metadata) {
    this._metadata.set(businessId, metadata);
  }

  /**
   * Get session metadata.
   * @param {string} businessId
   * @returns {object | undefined}
   */
  getMetadata(businessId) {
    return this._metadata.get(businessId);
  }

  /**
   * Remove a client from memory (does not destroy the WA session).
   * @param {string} businessId
   */
  remove(businessId) {
    this._clients.delete(businessId);
    this._statuses.delete(businessId);
    this._metadata.delete(businessId);
    this._qrCodes.delete(businessId);
    logger.info(`Session removed from memory: ${businessId}`, 'SessionManager');
  }

  /**
   * Destroy a client session completely (logout + remove).
   * @param {string} businessId
   */
  async destroy(businessId) {
    const client = this._clients.get(businessId);
    if (client) {
      try {
        await client.destroy();
        logger.info(`WhatsApp client destroyed: ${businessId}`, 'SessionManager');
      } catch (error) {
        logger.error(`Error destroying client: ${businessId}`, 'SessionManager', error);
      }
    }
    this._statuses.set(businessId, SessionStatus.DESTROYED);
    this.remove(businessId);
  }

  /**
   * List all sessions with their statuses.
   * @returns {Array<{business_id: string, session_id: string, status: string}>}
   */
  listSessions() {
    const sessions = [];
    for (const [businessId, status] of this._statuses.entries()) {
      sessions.push({
        business_id: businessId,
        session_id: businessId,
        status,
        metadata: this._metadata.get(businessId) || null,
      });
    }
    return sessions;
  }

  /**
   * Gracefully shutdown all clients.
   */
  async shutdownAll() {
    logger.info(`Shutting down ${this._clients.size} session(s)...`, 'SessionManager');
    const promises = [];
    for (const [businessId] of this._clients.entries()) {
      promises.push(this.destroy(businessId));
    }
    await Promise.allSettled(promises);
    logger.info('All sessions shut down.', 'SessionManager');
  }
}

// Singleton instance
const sessionManager = new SessionManager();

module.exports = { sessionManager, SessionStatus };
