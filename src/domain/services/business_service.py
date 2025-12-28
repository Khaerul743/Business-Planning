from supabase import AsyncClient

from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.core.context.request_context import current_user_id
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.models.businesses import Business
from src.domain.repositories import BusinessRepository
from src.domain.usecases.business import AddBusiness, AddBusinessInput

from .base import BaseService


class BusinessService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db
        self.business_repo = BusinessRepository(db)

        # usecases
        self.add_business_usecase = AddBusiness(self.business_repo)

    async def get_current_business(self):
        result = await self.business_repo.get_business_by_contextvar()
        if result is None:
            raise BusinessNotFound()

        return result

    async def add_new_business(self, payload: AddBusinessIn) -> Business:
        user_id = current_user_id.get()
        if user_id is None:
            raise Exception("User id is not found")

        result = await self.add_business_usecase.execute(
            AddBusinessInput(user_id, payload)
        )

        if not result.is_success():
            self.raise_error_usecase(result)
        data_business = result.get_data()

        if data_business is None:
            raise RuntimeError("Add business usecase did not returned data")

        return data_business.business_data

    async def update_business(self, payload: BusinessUpdateIn):
        user_id = current_user_id.get()
        if user_id is None:
            raise Exception("User id is not found")

        response = await self.business_repo.update_business(user_id, payload)
        return response
