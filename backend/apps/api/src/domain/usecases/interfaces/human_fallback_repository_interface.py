from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.human_fallback_schema import InsertNewHumanFallback
from src.domain.models import Human_Fallback


class IHumanFallbackRepository(ABC):
    @abstractmethod
    async def get_all_human_fallback_by_business_id(
        self, business_id: UUID
    ) -> list[Human_Fallback] | None:
        pass

    @abstractmethod
    async def get_human_fallback_by_id(
        self, conversation_id: UUID
    ) -> Human_Fallback | None:
        pass

    @abstractmethod
    async def get_or_insert_new_human_fallback(
        self, payload: InsertNewHumanFallback
    ) -> Human_Fallback:
        pass

    @abstractmethod
    async def delete_human_fallback_by_conversation_id(
        self, conversation_id: UUID
    ) -> Human_Fallback | None:
        pass
