from uuid import UUID
from abc import ABC, abstractmethod
from src.app.validators.insight_schema import AddInsight, AddGapKnowlage
from src.domain.models import Insight, GapKnowladge


class IInsightRepository(ABC):
    @abstractmethod
    async def createInsight(self, business_id: UUID, payload: AddInsight) -> Insight:
        pass

    @abstractmethod
    async def get_current_insight(self, business_id: UUID) -> None | Insight:
        pass

    @abstractmethod
    async def get_current_gap(self, business_id: UUID) -> None | GapKnowladge:
        pass

    @abstractmethod
    async def insert_gap_knowladge(
        self, business_id: UUID, payload: AddGapKnowlage
    ) -> GapKnowladge:
        pass
