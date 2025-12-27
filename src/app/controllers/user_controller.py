from supabase import AsyncClient

from src.core.exceptions import UnauthorizedException
from src.domain.services import UserService

from .base import BaseController


class UserController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.user_service = UserService(db)

    async def get_current_user(self):
        try:
            return await self.user_service.get_current_user()
        except UnauthorizedException as e:
            raise e
