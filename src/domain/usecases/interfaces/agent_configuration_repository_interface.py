from abc import ABC, abstractmethod

from src.app.validators.agent_schema import AgentConf
from src.domain.models import Agent_configuration


class IAgentConfigurationRepository(ABC):
    @abstractmethod
    async def get_agent_conf_by_agent_id(
        self, agent_id: int
    ) -> Agent_configuration | None:
        pass

    @abstractmethod
    async def insert_agent_conf(
        self, agent_id: int, agent_conf: AgentConf
    ) -> Agent_configuration:
        pass
