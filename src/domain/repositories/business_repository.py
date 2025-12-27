from postgrest.base_request_builder import SingleAPIResponse
from supabase import AsyncClient

from src.app.validators.business_schema import AddBusinessIn
from src.domain.models import Business
from src.domain.usecases.interfaces import IBusinessRepository


class BusinessRepository(IBusinessRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def add_business(
        self, user_id: int, data_business: AddBusinessIn
    ) -> Business:
        payload = {
            "user_id": user_id,
            "name": data_business.name,
            "owner_name": data_business.owner_name,
            "phone_number": data_business.phone_number,
        }
        result = await self.db.table("Businesses").insert(payload).execute()

        return Business.model_validate(result.data[0])
