from supabase import AsyncClient

from src.app.validators.auth_schema import RegisterIn, RegisterOut
from src.core.exceptions.auth_exception import (
    EmailAlreadyExistsException,
    EmailNotFoundException,
    InvalidCredentialsException,
    InvalidEmailFormatException,
    PasswordTooWeakException,
    RemoveTokenError,
    ValidationException,
)
from src.domain.services import AuthService

from .base import BaseController


class AuthController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.auth_service = AuthService(db)

    async def register_new_user(self, payload: RegisterIn) -> RegisterOut:
        try:
            result = await self.auth_service.register_new_user(payload)
            return result

        except EmailAlreadyExistsException as e:
            # Email already exists
            self._logger.debug(f"Email already exists: {type(e).__name__}")
            raise e
        except (
            InvalidEmailFormatException,
            PasswordTooWeakException,
            ValidationException,
        ) as e:
            # Validation errors
            self._logger.debug(f"Validation error: {type(e).__name__}")
            raise e
        except Exception as e:
            self._logger.error(f"Unexpected error while register new user: {str(e)}")
            raise e
