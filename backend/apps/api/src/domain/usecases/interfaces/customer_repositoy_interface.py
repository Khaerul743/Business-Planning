from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.customer_schema import InsertNewCustomer
from src.domain.models import Customers


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_or_insert_custormer(
        self, agent_id: UUID, customer_data: InsertNewCustomer
    ) -> tuple[Customers, bool]:
        pass

    @abstractmethod
    async def get_all_customer_by_agent_id(self, agent_id: UUID) -> list[Customers]:
        pass

    @abstractmethod
    async def get_all_customer_by_business_id(
        self, business_id: UUID
    ) -> list[Customers]:
        pass

    @abstractmethod
    async def get_customer_status_agent_by_agent_id(
        self, agent_id: UUID
    ) -> bool | None:
        pass

    @abstractmethod
    async def get_phone_number_by_conversation_id(
        self, conversation_id: UUID
    ) -> str | None:
        pass

    @abstractmethod
    async def get_customer_status_agent_by_customer_id(
        self, customer_id: UUID
    ) -> bool | None:
        pass

    @abstractmethod
    async def update_customer_status_agent_by_customer_id(
        self, customer_id: UUID, status: bool
    ) -> Customers | None:
        pass
