from supabase import AsyncClient

from domain.models.businesses import Business
from src.app.validators.business_schema import AddBusinessIn
from src.domain.repositories import BusinessRepository
from src.domain.usecases.business import AddBusiness, AddBusinessInput

from .base import BaseService


class BusinessService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db
        self.business_repo = BusinessRepository(db)

        # usecases
        self.add_business_usecase = AddBusiness(self.business_repo)

    async def add_new_business(self, payload: AddBusinessIn) -> Business:
        try:
            result = await self.add_business_usecase.execute(
                AddBusinessInput(1, payload)
            )
            if not result.is_success():
                self.raise_error_usecase(result)

            data_business = result.get_data()
            if data_business is None:
                raise RuntimeError("Add business usecase did not returned data")

            return data_business.business_data

        except RuntimeError as e:
            raise e
        except Exception as e:
            raise e
