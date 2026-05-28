from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from src.app.validators.analytic_schema import InsertAgentAnalytic
from src.domain.models import AgentAnalytics


class IAnalyticRepository(ABC):
    @abstractmethod
    async def get_agent_analytics(self, agent_id: UUID) -> list[AgentAnalytics] | None:
        pass

    @abstractmethod
    async def insert_agent_analytic(
        self, agent_id: UUID, payload: InsertAgentAnalytic
    ) -> AgentAnalytics:
        pass

    async def get_token_usage_trend(self, agent_id: UUID) -> list[dict] | None:
        pass

    @abstractmethod
    async def get_message_usage_trend(self, agent_id: UUID) -> list[dict] | None:
        pass

    @abstractmethod
    async def get_human_vs_ai_message_trend(self, agent_id: UUID) -> list[dict] | None:
        pass

    @abstractmethod
    async def get_category_messages(
        self,
        agent_id: UUID,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[dict] | None:
        pass

    @abstractmethod
    async def get_knowladge_gap(self, agent_id: UUID) -> None | list[dict]:
        pass
