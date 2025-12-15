from supabase import AsyncClient

from src.app.validators.auth_schema import RegisterIn, RegisterOut
from src.core.utils.hash import PasswordHashed
from src.domain.repositories import UserRepository
from src.domain.usecases.auth import (
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

        # Use case
        self.register_validation = RegisterValidation()
        self.register_new_user_usecase = RegisterNewUser(
            self.user_repo, self.register_validation, self.password_hashed
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
