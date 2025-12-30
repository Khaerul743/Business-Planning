from postgrest.base_request_builder import SingleAPIResponse
from supabase import AsyncClient

from src.core.context.request_context import current_user_id
from src.domain.models import User
from src.domain.usecases.interfaces import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_user_by_business_id(self, business_id: int) -> User | None:
        user_id = current_user_id.get()
        result = (
            await self.db.table("Businesses")
            .select("Users(*)")
            .eq("id", business_id)
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            return None

        print(result.data["Users"])

        return User.model_validate(result.data["Users"])

    async def get_all_users(self) -> list[User]:
        result = await self.db.table("Users").select("*").execute()
        return [User.model_validate(row) for row in result.data]

    async def get_user_by_id(self, user_id: int) -> User | None:
        result: SingleAPIResponse | None = (
            await self.db.table("Users")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return User.model_validate(result.data)

    async def get_by_context_user(self) -> User | None:
        user_id = current_user_id.get()
        result: SingleAPIResponse | None = (
            await self.db.table("Users")
            .select("*")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return User.model_validate(result.data)

    async def get_user_by_email(self, email: str) -> User | None:
        result = (
            await self.db.table("Users")
            .select("*")
            .eq("email", email)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return User.model_validate(result.data)

    async def create_user(
        self,
        name: str,
        email: str,
        hashed_password: str,
    ) -> User | None:
        payload = {
            "name": name,
            "email": email,
            "password": hashed_password,
        }

        result = await self.db.table("Users").insert(payload).execute()

        if result.data is None:
            return None

        return User.model_validate(result.data[0])
