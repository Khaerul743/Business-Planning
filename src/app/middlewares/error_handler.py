# src/core/handlers/exceptions.py (atau di main.py)

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import BaseCustomeException
from src.core.utils import error_response, get_logger

logger = get_logger(__name__)


# --- 1. Handler untuk RequestValidationError (Validation/Pydantic Error) ---
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Menangkap Pydantic validation error (422)."""

    logger.warning(f"Validation Error: {exc.errors()}")

    # Memformat errors() dari Pydantic/FastAPI ke struktur details yang konsisten
    details = [
        # Mengambil lokasi field (misalnya 'body', 'name')
        {"field": ".".join(map(str, err["loc"][1:])), "error": err["msg"]}
        for err in exc.errors()
    ]

    return error_response(
        http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_FAILED",
        message="The request data failed validation checks.",
        details=details,
    )


# --- 2. Handler untuk SQLAlchemyError (Database Error) ---
async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    """Menangkap error dari SQLAlchemy (Database)."""

    logger.error(f"Database error: {str(exc)}", exc_info=True)

    return error_response(
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="DB_INTERNAL_ERROR",
        message="Internal error while processing database request.",
    )


# --- 3. Handler untuk BaseCustomeException (Custom Errors) ---
async def custom_exception_handler(request: Request, exc: BaseCustomeException):
    """Menangkap semua Custom Exception yang di-raise dari aplikasi."""

    # Log level ERROR karena ini adalah error yang sengaja kita definisikan
    logger.error(f"Custom Error: {exc.detail.get('code', 'UNKNOWN')}", exc_info=False)

    return error_response(
        http_status=exc.status_code,
        error_code=exc.detail.get("code", "CUSTOM_ERROR"),
        message=exc.detail.get("message", "A defined custom error occurred."),
        details=exc.detail.get("details")
        if isinstance(exc.detail, dict) and "details" in exc.detail
        else None,
    )


# --- 4. Handler untuk Exception (Catch-All) ---
async def unexpected_exception_handler(request: Request, exc: Exception):
    """Menangkap semua Exception Python yang tidak spesifik tertangkap."""

    logger.exception(f"Unexpected error: {str(exc)}")

    return error_response(
        http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code="UNEXPECTED_SERVER_ERROR",
        message="An unexpected server error occurred.",
    )
