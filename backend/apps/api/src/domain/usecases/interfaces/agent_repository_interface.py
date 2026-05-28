from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.agent_schema import InsertAgent
from src.domain.models import Agents


class IAgentRepository(ABC):
    @abstractmethod
    async def get_agent_by_phone_number_id(self, phone_number_id: str) -> Agents | None:
        pass

    @abstractmethod
    async def get_agent_id_by_user_id(self, business_id: UUID) -> UUID | None:
        pass

    @abstractmethod
    async def get_agent_by_id(self, id: UUID) -> Agents | None:
        pass

    @abstractmethod
    async def get_agent_by_user_id(self, user_id: UUID) -> Agents | None:
        pass

    @abstractmethod
    async def get_agent_by_business_id(self, business_id: UUID) -> Agents | None:
        pass

    @abstractmethod
    async def get_status_agent(self, agent_id: UUID) -> bool | None:
        pass

    @abstractmethod
    async def create_agent_by_business_id(
        self, business_id: UUID, agent_data: InsertAgent
    ) -> Agents:
        pass

    @abstractmethod
    async def update_status_agent(self, agent_id: UUID, status: bool) -> Agents | None:
        pass

    @abstractmethod
    async def update_name_agent(self, agent_id: UUID, name: str) -> str:
        pass
