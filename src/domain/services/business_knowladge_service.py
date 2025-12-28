from supabase import AsyncClient

from src.app.validators.business_knowladge_schema import AddBusinessKnowladgeIn
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.repositories import BusinessKnowladgeRepository, BusinessRepository

from .base import BaseService


class BusinessKnowladgeService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        self.business_knowladge_repo = BusinessKnowladgeRepository(self.db)
        self.business_repo = BusinessRepository(self.db)

    async def add_business_knowladge(
        self, business_id: int, payload: AddBusinessKnowladgeIn
    ):
        try:
            business = await self.business_repo.get_business_by_id(business_id)
            if business is None:
                raise BusinessNotFound(f"Business not found with id {business_id}")

            response_data = await self.business_knowladge_repo.add_business_knowladge(
                business_id, payload
            )
            return response_data
        except BusinessNotFound as e:
            self.logger.warning(str(e))
            raise e
