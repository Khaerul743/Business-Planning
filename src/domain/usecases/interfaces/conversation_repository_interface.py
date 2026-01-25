from abc import ABC, abstractmethod
from typing import Literal

from src.domain.models import Conversations


class IConversationRepository(ABC):
    @abstractmethod
    async def insert_new_conversation(
        self, customer_id: int, status: Literal["active", "inactive"] = "active"
    ) -> Conversations:
        pass

    @abstractmethod
    async def get_or_create_conversation(
        self,
        business_id: int | None,
        agent_id: int,
        customer_id: int,
        status: Literal["active", "inactive"] = "active",
    ) -> Conversations:
        pass

    @abstractmethod
    async def get_all_conversations_by_business_id(
        self, business_id: int
    ) -> list[Conversations] | None:
        pass
