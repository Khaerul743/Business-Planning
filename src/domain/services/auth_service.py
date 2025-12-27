from typing import Literal

from fastapi import Request, Response
from supabase import AsyncClient

from src.app.validators.auth_schema import LoginIn, LoginOut, RegisterIn, RegisterOut
from src.core.exceptions import UnauthorizedException
from src.core.utils.hash import PasswordHashed
from src.core.utils.security import jwtHandler
from src.domain.repositories import UserRepository
from src.domain.usecases.auth import (
    AuthenticateInput,
    AuthenticateUser,
    RegisterNewUser,
    RegisterValidation,
    RegisterValidationInput,
)

from .base import BaseService


class AuthService(BaseService):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)

        # DB Session
        self.db = db
        self.user_repo = UserRepository(self.db)

        # Dependencies
        self.password_hashed = PasswordHashed()
        self.jwt_handler = jwtHandler

        # JWT Conf
        self.access_token = "access_token"
        self.refresh_token = "refresh_token"
        self.httponly = True
        self.secure = False
        self.samesite: Literal["lax", "strict", "none"] = "lax"

        # Use case
        self.register_validation = RegisterValidation()
        self.register_new_user_usecase = RegisterNewUser(
            self.user_repo, self.register_validation, self.password_hashed
        )
        self.authenticate_usecase = AuthenticateUser(
            self.user_repo, self.jwt_handler, self.password_hashed
        )

    async def register_new_user(self, payload: RegisterIn) -> RegisterOut:
        input_data = RegisterValidationInput(
            name=payload.name, password=payload.password, email=payload.email
        )

        # Delegate validation and creation to use case
        reg_user = await self.register_new_user_usecase.execute(input_data)
        if not reg_user:
            self.logger.warning(
                f"Register user failed: code={reg_user.get_error_code()} error={reg_user.get_error()}"
            )
            self.raise_error_usecase(reg_user)

        user = reg_user.get_data()
        if user is None:
            raise RuntimeError("register new user usecase doesn't returned data")

        return RegisterOut(name=str(user.name), email=str(user.email))

    async def login_handler(self, response: Response, payload: LoginIn) -> LoginOut:
        """
        Authenticate user with email and password.

        Args:
            email: User email
            password: User password

        Returns:
            User object if authentication successful

        Raises:
            EmailNotFoundException: If email is not found
            InvalidCredentialsException: If password is incorrect
            DatabaseException: If database operation fails
        """
        auth_user = await self.authenticate_usecase.execute(
            AuthenticateInput(payload.email, payload.password)
        )
        if not auth_user:
            self.logger.warning(
                f"{payload.email} login failed: {auth_user.get_error()}"
            )
            self.raise_error_usecase(auth_user)
        # Set cookie
        get_data_user = auth_user.get_data()
        if get_data_user:
            user_data = {
                "id": get_data_user.id,
                "email": get_data_user.email,
                "role": get_data_user.role,
            }
        else:
            raise RuntimeError("authenticate usecase did not returned data")

        access_token = self.jwt_handler.create_access_token(user_data)
        refresh_token = self.jwt_handler.create_refresh_token(str(get_data_user.id))

        response.set_cookie(
            key=self.access_token,
            value=access_token,
            httponly=self.httponly,
            secure=self.secure,  # True (HTTPS)
            samesite=self.samesite,
            max_age=3600,  # One hour
        )

        response.set_cookie(
            key=self.refresh_token,
            value=refresh_token,
            httponly=self.httponly,
            secure=self.secure,
            max_age=60 * 60 * 24 * 7,  # 7 hari
            samesite=self.samesite,
        )

        return LoginOut(
            name=get_data_user.name, email=get_data_user.email, role=get_data_user.role
        )

    async def refresh_access_token(self, request: Request, response: Response):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise UnauthorizedException("Missing refresh token")

        payload = self.jwt_handler.verify_token(refresh_token)
        if not payload:
            raise UnauthorizedException("Invalid refresh token")

        elif payload["type"] != "refresh":
            raise UnauthorizedException("Invalid token type")

        user = await self.user_repo.get_user_by_id(payload["sub"])
        if user is None:
            raise UnauthorizedException("Invalid user id")

        new_access_token = self.jwt_handler.create_access_token(
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
            }
        )

        response.set_cookie(
            key=self.access_token,
            value=new_access_token,
            httponly=self.httponly,
            secure=self.secure,
            max_age=900,
            samesite=self.samesite,
        )

        return {"status": "success"}

    def remove_cookie_tokens(self, response: Response) -> dict[str, str]:
        # Remove access token
        response.delete_cookie(self.access_token)

        # Remove refresh token
        response.delete_cookie(self.refresh_token)
        return {"status": "success"}
