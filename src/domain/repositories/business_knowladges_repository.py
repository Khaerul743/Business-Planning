from supabase import AsyncClient

from app.validators.business_knowladge_schema import AddBusinessKnowladgeIn
from domain.models import BusinessKnowladge
from src.core.utils.logger import get_logger
from src.domain.usecases.interfaces import IBusinessKnowladgeRepository


class BusinessKnowladgeRepository(IBusinessKnowladgeRepository):
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

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
