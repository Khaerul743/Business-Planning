from supabase import AsyncClient

from src.domain.models import User


class UserRepository:
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_all_users(self) -> list[User]:
        result = await self.db.table("Users").select("*").execute()
        return [User.model_validate(row) for row in result.data]

    async def get_user_by_id(self, user_id: int) -> User | None:
        result = (
            await self.db.table("Users")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return User.model_validate(result.data)
