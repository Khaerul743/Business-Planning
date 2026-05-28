from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.domain.models import Business


class IBusinessRepository(ABC):
    @abstractmethod
    async def get_business_by_id(self, business_id: UUID) -> Business | None:
        pass

    @abstractmethod
    async def get_business_id_n_agent_id_by_user_id(
        self, user_id: UUID
    ) -> tuple[UUID | None, UUID | None]:
        pass

    @abstractmethod
    async def add_business(
        self, user_id: UUID, data_business: AddBusinessIn
    ) -> Business:
        pass

    @abstractmethod
    async def update_business_by_id(
        self, business_id: UUID, business_data: BusinessUpdateIn
    ) -> Business:
        pass

    @abstractmethod
    async def update_business_by_user_id(
        self, user_id: UUID, business_data: BusinessUpdateIn
    ) -> Business:
        pass
