from supabase import AsyncClient

from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.services import BusinessKnowladgeService

from .base import BaseController


class BusinessKnowladgeController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.business_knowladge_service = BusinessKnowladgeService(db)

    async def get_all_business_knowladge_by_business_id_handler(self):
        try:
            business_knowladges = await self.business_knowladge_service.get_all_business_knowladge_by_business_id()
            list_data = []
            if business_knowladges is not None:
                for i in business_knowladges:
                    list_data.append(i.model_dump())

            return list_data
        except Exception as e:
            self._logger.error(f"Unexpected error: {str(e)}")
            raise e

    async def add_business_knowladge_handler(self, payload: AddBusinessKnowladgeIn):
        try:
            result = await self.business_knowladge_service.add_business_knowladge(
                payload
            )
            return result.model_dump()
        except Exception as e:
            self._logger.error(f"Unexpected error: {str(e)}")
            raise e

    async def update_business_knowladge_handler(
        self, business_knowladge_id: int, payload: UpdateBusinessKnowladgeIn
    ):
        try:
            result = await self.business_knowladge_service.update_business_knowladge(
                business_knowladge_id, payload
            )
            return result.model_dump()
        except UnauthorizedException as e:
            self._logger.warning(str(e))
            raise e
        except BusinessNotFound as e:
            self._logger.warning(str(e))
            raise e
