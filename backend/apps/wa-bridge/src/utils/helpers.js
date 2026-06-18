/**
 * Helper Utilities
 *
 * Common helper functions used across the application.
 */

/**
 * Sleep for a given number of milliseconds.
 * @param {number} ms - Milliseconds to sleep.
 * @returns {Promise<void>}
 */
function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Generate a random delay between min and max milliseconds.
 * @param {number} min - Minimum delay in ms. Default: 2000
 * @param {number} max - Maximum delay in ms. Default: 5000
 * @returns {number}
 */
function randomDelay(min = 2000, max = 5000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Format a phone number to WhatsApp chat ID format.
 * Ensures the number ends with @c.us for personal chats.
 * @param {string} phoneNumber - The phone number to format.
 * @returns {string} WhatsApp chat ID.
 */
function formatChatId(phoneNumber) {
  if (!phoneNumber) return '';
  // Already formatted
  if (phoneNumber.includes('@')) return phoneNumber;
  // Remove non-digit characters
  const cleaned = phoneNumber.replace(/\D/g, '');
  return `${cleaned}@c.us`;
}

/**
 * Extract clean phone number from WhatsApp chat ID.
 * @param {string} chatId - WhatsApp chat ID (e.g., "628123456789@c.us")
 * @returns {string} Clean phone number.
 */
function extractPhoneNumber(chatId) {
  if (!chatId) return '';
  return chatId.replace('@c.us', '').replace('@s.whatsapp.net', '');
}

module.exports = {
  sleep,
  randomDelay,
  formatChatId,
  extractPhoneNumber,
};
