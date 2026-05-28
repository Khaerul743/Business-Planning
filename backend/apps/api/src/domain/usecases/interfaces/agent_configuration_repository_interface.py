from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.agent_schema import AgentConf, UpdateAgentIn
from src.domain.models import Agent_configuration


class IAgentConfigurationRepository(ABC):
    @abstractmethod
    async def get_agent_conf_by_agent_id(
        self, agent_id: UUID
    ) -> Agent_configuration | None:
        pass

    @abstractmethod
    async def insert_agent_conf(
        self, agent_id: UUID, agent_conf: AgentConf
    ) -> Agent_configuration:
        pass

    @abstractmethod
    async def update_agent_conf(
        self, agent_id: UUID, payload: UpdateAgentIn
    ) -> Agent_configuration | None:
        pass
