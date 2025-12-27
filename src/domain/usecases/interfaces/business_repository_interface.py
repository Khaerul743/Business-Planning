from abc import ABC, abstractmethod

from src.app.validators.business_schema import AddBusinessIn
from src.domain.models import Business


class IBusinessRepository(ABC):
    @abstractmethod
    async def add_business(
        self, user_id: int, data_business: AddBusinessIn
    ) -> Business:
        pass
