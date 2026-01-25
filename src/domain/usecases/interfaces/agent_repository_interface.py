from abc import ABC, abstractmethod

from src.app.validators.agent_schema import InsertAgent
from src.domain.models import Agents


class IAgentRepository(ABC):
    @abstractmethod
    async def get_agent_by_phone_number_id(self, phone_number_id: str) -> Agents | None:
        pass

    @abstractmethod
    async def get_agent_id_by_user_id(self, business_id: int) -> int | None:
        pass

    @abstractmethod
    async def create_agent_by_business_id(
        self, business_id: int, agent_data: InsertAgent
    ) -> Agents:
        pass
