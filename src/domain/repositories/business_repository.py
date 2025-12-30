from postgrest import APIResponse
from postgrest.base_request_builder import SingleAPIResponse
from supabase import AsyncClient

from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.core.context.request_context import current_user_id
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.core.utils.logger import get_logger
from src.domain.models import Business
from src.domain.usecases.interfaces import IBusinessRepository


class BusinessRepository(IBusinessRepository):
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def get_business_by_id(self, business_id: int) -> Business | None:
        result = (
            await self.db.table("Businesses")
            .select("*")
            .eq("id", business_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return Business.model_validate(result.data)

    async def get_business_id_by_user_id(self, user_id: int) -> int | None:
        try:
            result = (
                await self.db.table("Businesses")
                .select("id")
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None

            return result.data["id"]

        except Exception as e:
            self._logger.error(f"Error while get business by user id: {str(e)}")
            raise e

    async def get_business_by_contextvar(self):
        user_id = current_user_id.get()
        result: SingleAPIResponse | None = (
            await self.db.table("Businesses")
            .select("*")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return Business.model_validate(result.data)

    async def add_business(
        self, user_id: int, data_business: AddBusinessIn
    ) -> Business:
        payload = {
            "user_id": user_id,
            "name": data_business.name,
            "owner_name": data_business.owner_name,
            "phone_number": data_business.phone_number,
        }
        result: APIResponse = (
            await self.db.table("Businesses").insert(payload).execute()
        )

        return Business.model_validate(result.data[0])

    async def update_business_by_id(
        self, business_id: int, business_data: BusinessUpdateIn
    ) -> Business:
        payload = business_data.dict(exclude_unset=True)
        result = (
            await self.db.table("Businesses")
            .update(payload)
            .eq("id", business_id)
            .execute()
        )

        return Business.model_validate(result.data[0])

    async def update_business_by_user_id(
        self, user_id: int, business_data: BusinessUpdateIn
    ) -> Business:
        payload = business_data.dict(exclude_unset=True)
        result = (
            await self.db.table("Businesses")
            .update(payload)
            .eq("user_id", user_id)
            .execute()
        )

        return Business.model_validate(result.data[0])
