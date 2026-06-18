/**
 * WhatsApp Event Handlers
 *
 * Registers all WhatsApp client event listeners for a given business.
 * Handles: qr, authenticated, auth_failure, ready, message, disconnected.
 */

const qrcodeTerminal = require('qrcode-terminal');
const QRCode = require('qrcode');
const logger = require('../utils/logger');
const { extractPhoneNumber } = require('../utils/helpers');
const { sessionManager, SessionStatus, fastapiEventService } = require('../services');

/**
 * Register all event handlers for a WhatsApp client instance.
 * @param {import('whatsapp-web.js').Client} client
 * @param {string} businessId
 */
function registerClientEvents(client, businessId) {
  // ─── QR Code Event ──────────────────────────────────────────────────────────
  client.on('qr', async (qr) => {
    logger.info(`QR Code generated for business: ${businessId}`, 'WhatsApp');
    qrcodeTerminal.generate(qr, { small: true });

    try {
      // Generate base64 QR code for API response
      const qrBase64 = await QRCode.toDataURL(qr);
      sessionManager.setQrCode(businessId, qrBase64);
      sessionManager.setStatus(businessId, SessionStatus.PENDING_QR);

      // Notify FastAPI
      await fastapiEventService.sendQrEvent(businessId, qrBase64);
    } catch (error) {
      logger.error('Failed to generate QR base64', 'WhatsApp', error);
      sessionManager.setQrCode(businessId, qr);

      // Fallback: send raw QR string if base64 conversion fails
      await fastapiEventService.sendQrEvent(businessId, qr);
    }
  });

  // ─── Authenticated Event ────────────────────────────────────────────────────
  client.on('authenticated', async () => {
    logger.info(`Session authenticated: ${businessId}`, 'WhatsApp');
    sessionManager.setStatus(businessId, SessionStatus.AUTHENTICATING);
    // Clear QR code since it's no longer needed
    sessionManager.setQrCode(businessId, null);

    // Notify FastAPI
    await fastapiEventService.sendAuthenticatingEvent(businessId);
  });

  // ─── Auth Failure Event ─────────────────────────────────────────────────────
  client.on('auth_failure', async (msg) => {
    logger.error(`Authentication failed for ${businessId}: ${msg}`, 'WhatsApp');
    sessionManager.setStatus(businessId, SessionStatus.DISCONNECTED);

    // Notify FastAPI
    await fastapiEventService.sendAuthFailureEvent(businessId, msg);
  });

  // ─── Ready Event ────────────────────────────────────────────────────────────
  client.on('ready', async () => {
    logger.info(`WhatsApp client ready: ${businessId}`, 'WhatsApp');
    sessionManager.setStatus(businessId, SessionStatus.CONNECTED);

    try {
      // Extract client metadata
      const info = client.info;
      const phoneNumber = info?.wid?.user || '';
      const displayName = info?.pushname || '';

      const metadata = {
        phone_number: phoneNumber,
        display_name: displayName,
        business_id: businessId,
        session_id: businessId,
      };

      sessionManager.setMetadata(businessId, metadata);

      // Notify FastAPI backend that the session is connected
      await fastapiEventService.sendReadyEvent(businessId, phoneNumber, displayName);
    } catch (error) {
      logger.error(
        `Failed to process ready event for ${businessId}`,
        'WhatsApp',
        error
      );
    }
  });

  // ─── Message Event ──────────────────────────────────────────────────────────
  client.on('message', async (msg) => {
    try {
      // Ignore group messages
      if (msg.from.includes('@g.us')) return;
      // Ignore self messages
      if (msg.fromMe) return;
      // Ignore status broadcasts
      if (msg.from === 'status@broadcast') return;

      const contact = await msg.getContact();
      const senderNumber = extractPhoneNumber(msg.from);
      const senderName = msg.notifyName || contact.pushname || 'Unknown';
      const contactDetail = JSON.stringify(contact, null, 2)
      console.log(contactDetail)
      console.log(contact.id.user)
      logger.info(
        `Incoming message from [${senderNumber}] (${senderName}): ${msg.body}`,
        `WA:${businessId}`
      );

      // Get business metadata for the payload
      const metadata = sessionManager.getMetadata(businessId) || {};

      // Build Meta WhatsApp API compatible payload
      const payload = {
        object: 'whatsapp_business_account',
        entry: [
          {
            changes: [
              {
                value: {
                  messaging_product: 'whatsapp',
                  metadata: {
                    display_phone_number: metadata.phone_number || '',
                    phone_number_id: businessId,
                    is_from_wa_service: true
                  },
                  contacts: [
                    {
                      profile: {
                        name: senderName,
                      },
                      wa_id: contact.id.user,
                    },
                  ],
                  messages: [
                    {
                      from: contact.id.user,
                      id: msg.id?._serialized || msg.id?.id || `msg_${Date.now()}`,
                      timestamp: String(msg.timestamp || Math.floor(Date.now() / 1000)),
                      type: 'text',
                      text: {
                        body: msg.body,
                      },
                    },
                  ],
                },
                field: 'messages',
              },
            ],
          },
        ],
      };

      // Forward to FastAPI
      await fastapiEventService.sendWebhook(payload);
    } catch (error) {
      logger.error(
        `Failed to process incoming message for ${businessId}`,
        'WhatsApp',
        error
      );
    }
  });

  // ─── Disconnected Event ─────────────────────────────────────────────────────
  client.on('disconnected', async (reason) => {
    logger.warn(`WhatsApp client disconnected: ${businessId} - Reason: ${reason}`, 'WhatsApp');
    sessionManager.setStatus(businessId, SessionStatus.DISCONNECTED);

    // Notify FastAPI
    await fastapiEventService.sendDisconnectedEvent(businessId, reason);
  });
}

module.exports = { registerClientEvents };
