from supabase import AsyncClient

from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.core.exceptions.business_knowladge_exception import BusinessKnowladgeNotFound
from src.core.utils.logger import get_logger
from src.domain.models import BusinessKnowladge
from src.domain.usecases.interfaces import IBusinessKnowladgeRepository


class BusinessKnowladgeRepository(IBusinessKnowladgeRepository):
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def get_all_business_knowladge_by_business_id(
        self, business_id: int
    ) -> list[BusinessKnowladge] | None:
        try:
            result = (
                await self.db.table("Business_knowladges")
                .select("*")
                .eq("business_id", business_id)
                .execute()
            )
            if result is None:
                return None

            data = result.data

            list_data = []
            for i in data:
                list_data.append(BusinessKnowladge.model_validate(i))

            return list_data
        except Exception as e:
            self._logger.error(f"Error while get business knowladges: {str(e)}")
            raise e

    async def add_business_knowladge(
        self, business_id: int, business_knowladge_data: AddBusinessKnowladgeIn
    ) -> BusinessKnowladge:
        try:
            payload = business_knowladge_data.dict()
            payload["business_id"] = business_id
            result = (
                await self.db.table("Business_knowladges").insert(payload).execute()
            )
            return BusinessKnowladge.model_validate(result.data[0])

        except Exception as e:
            self._logger.error(f"Error while add business knowladge: {str(e)}")
            raise e

    async def update_business_knowladge_by_id(
        self,
        business_knowladge_id: int,
        business_knowladge_data: UpdateBusinessKnowladgeIn,
    ) -> BusinessKnowladge:
        try:
            payload = business_knowladge_data.dict(exclude_unset=True)
            result = (
                await self.db.table("Business_knowladges")
                .update(payload)
                .eq("id", business_knowladge_id)
                .execute()
            )
            if len(result.data) == 0:
                raise BusinessKnowladgeNotFound()
            return BusinessKnowladge.model_validate(result.data[0])
        except BusinessKnowladgeNotFound as e:
            self._logger.warning(f"{str(e)}")
            raise e
