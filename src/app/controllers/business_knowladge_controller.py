from supabase import AsyncClient

from src.app.validators.business_knowladge_schema import AddBusinessKnowladgeIn
from src.domain.services import BusinessKnowladgeService

from .base import BaseController


class BusinessKnowladgeController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.business_knowladge_service = BusinessKnowladgeService(db)

    async def add_business_knowladge_handler(
        self, business_id: int, payload: AddBusinessKnowladgeIn
    ):
        try:
            result = await self.business_knowladge_service.add_business_knowladge(
                business_id, payload
            )
            return result.model_dump()
        except Exception as e:
            self._logger.error(f"Unexpected error: {str(e)}")
            raise e
