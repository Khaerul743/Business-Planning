from abc import ABC, abstractmethod

from src.app.validators.agent_schema import CreateAgentIn
from src.domain.models import Agents


class IAgentRepository(ABC):
    @abstractmethod
    async def get_agent_id_by_user_id(self, business_id: int) -> int | None:
        pass

    @abstractmethod
    async def create_agent_by_business_id(
        self, business_id: int, agent_data: CreateAgentIn
    ) -> Agents:
        pass
