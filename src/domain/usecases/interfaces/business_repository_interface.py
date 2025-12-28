from abc import ABC, abstractmethod

from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.domain.models import Business


class IBusinessRepository(ABC):
    @abstractmethod
    async def get_business_by_id(self, business_id: int) -> Business | None:
        pass

    @abstractmethod
    async def add_business(
        self, user_id: int, data_business: AddBusinessIn
    ) -> Business:
        pass

    @abstractmethod
    async def update_business(
        self, user_id: int, business_data: BusinessUpdateIn
    ) -> Business:
        pass
