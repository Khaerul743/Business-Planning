from fastapi import Request, Response
from supabase import AsyncClient

from src.app.validators.auth_schema import LoginIn, RegisterIn, RegisterOut
from src.core.exceptions import UnauthorizedException
from src.core.exceptions.auth_exception import (
    EmailAlreadyExistsException,
    EmailNotFoundException,
    InvalidCredentialsException,
    InvalidEmailFormatException,
    PasswordTooWeakException,
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
            raise e
        except (
            InvalidEmailFormatException,
            PasswordTooWeakException,
            ValidationException,
        ) as e:
            raise e
        except Exception as e:
            raise e

    async def login_handler(self, response: Response, payload: LoginIn):
        try:
            result = await self.auth_service.login_handler(response, payload)
            return result
        except (EmailNotFoundException, InvalidCredentialsException) as e:
            # Re-raise custom exceptions
            raise e
        except Exception as e:
            raise e

    async def refresh_token_handler(self, request: Request, response: Response):
        try:
            res = await self.auth_service.refresh_access_token(request, response)
            return res
        except UnauthorizedException as e:
            self._logger.warning(str(e))
            raise e
        except Exception as e:
            self._logger.error(str(e))
            raise e

    async def logout_handler(self, response: Response) -> dict[str, str]:
        try:
            return self.auth_service.remove_cookie_tokens(response)

        except Exception as e:
            self._logger.error(str(e))
            raise e
