from supabase import AsyncClient

from src.core.exceptions import UnauthorizedException
from src.domain.repositories import UserRepository

from .base import BaseService


class UserService(BaseService):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.user_repo = UserRepository(db)

    async def get_current_user(self):
        user = await self.user_repo.get_by_context_user()
        if user is None:
            raise UnauthorizedException()

        return user
