from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.exceptions import BaseCustomeException
from src.core.utils import error_response, get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except BaseCustomeException as e:
            logger.exception(f"Error from custome exceptions: {str(e)}")
            return error_response(
                http_status=e.status_code,
                error_code=e.detail.get("code", "UNKNOWN"),
                message=e.detail.get("message", ""),
            )

        except RequestValidationError as e:
            logger.warning(f"Validation error: {e.errors()}")
            # Memformat errors() menjadi list of dict yang konsisten
            details = [
                {"field": ".".join(map(str, err["loc"][1:])), "error": err["msg"]}
                for err in e.errors()
            ]
            return error_response(
                http_status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_code="VALIDATION_FAILED",
                message="The request data failed validation.",
                details=details,
            )

        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}", exc_info=True)
            return error_response(
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code="DB_INTERNAL_ERROR",
                message="Internal error while processing database request.",
            )

        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return error_response(
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_code="UNEXPECTED_SERVER_ERROR",
                message="An unexpected server error occurred.",
            )
