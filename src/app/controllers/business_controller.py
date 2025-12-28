from supabase import AsyncClient

from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.services import BusinessService

from .base import BaseController


class BusinessController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.business_service = BusinessService(db)

    async def get_current_business_handler(self):
        try:
            result = await self.business_service.get_current_business()
            return result
        except BusinessNotFound as e:
            self._logger.warning(str(e))
            raise e
        except Exception as e:
            self._logger.error(str(e))
            raise e

    async def add_new_business_handler(self, payload: AddBusinessIn):
        try:
            result = await self.business_service.add_new_business(payload)
            return result
        except RuntimeError as e:
            self._logger.error(str(e))
            raise e
        except Exception as e:
            self._logger.error(str(e))
            raise e

    async def update_business_handler(self, payload: BusinessUpdateIn):
        try:
            result = await self.business_service.update_business(payload)
            return result
        except Exception as e:
            self._logger.error(str(e))
            raise e
