/**
 * WA-Bridge Application Entry Point
 *
 * WhatsApp Gateway / Bridge for AI Customer Service Platform.
 * This service acts as a gateway connecting WhatsApp with a FastAPI backend.
 *
 * Responsibilities:
 *   1. Manage WhatsApp connections (multi-tenant)
 *   2. Forward incoming messages to FastAPI
 *   3. Receive responses from FastAPI
 *   4. Send messages via WhatsApp
 */

const express = require('express');
const { env } = require('./config');
const logger = require('./utils/logger');
const routes = require('./routes');
const { errorHandler, requestLogger } = require('./middlewares');
const { sessionManager } = require('./services');

// ─── Create Express App ────────────────────────────────────────────────────────
const app = express();

// ─── Global Middlewares ────────────────────────────────────────────────────────
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));
app.use(requestLogger);

// ─── API Routes ────────────────────────────────────────────────────────────────
app.use('/api', routes);

// ─── 404 Handler ───────────────────────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({
    success: false,
    error: {
      code: 'NOT_FOUND',
      message: `Route ${req.method} ${req.originalUrl} not found`,
    },
  });
});

// ─── Global Error Handler ──────────────────────────────────────────────────────
app.use(errorHandler);

// ─── Start Server ──────────────────────────────────────────────────────────────
const server = app.listen(env.port, () => {
  logger.info('═══════════════════════════════════════════════', 'App');
  logger.info('  WA-Bridge Service Started', 'App');
  logger.info(`  Environment : ${env.nodeEnv}`, 'App');
  logger.info(`  Port        : ${env.port}`, 'App');
  logger.info(`  FastAPI URL : ${env.fastApiUrl}`, 'App');
  logger.info(`  Session Path: ${env.sessionPath}`, 'App');
  logger.info('═══════════════════════════════════════════════', 'App');
});

// ─── Graceful Shutdown ─────────────────────────────────────────────────────────
async function gracefulShutdown(signal) {
  logger.info(`${signal} received. Starting graceful shutdown...`, 'App');

  // Close HTTP server
  server.close(() => {
    logger.info('HTTP server closed.', 'App');
  });

  // Destroy all WhatsApp sessions
  await sessionManager.shutdownAll();

  logger.info('Graceful shutdown complete.', 'App');
  process.exit(0);
}

process.on('SIGINT', () => gracefulShutdown('SIGINT'));
process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception', 'App', error);
  process.exit(1);
});

process.on('unhandledRejection', (reason) => {
  logger.error(`Unhandled Rejection: ${reason}`, 'App');
});

module.exports = app;
