from abc import ABC, abstractmethod
from typing import Literal
from uuid import UUID

from src.domain.models import Conversations


class IConversationRepository(ABC):
    @abstractmethod
    async def get_conversation_by_id(
        self, conversation_id: UUID
    ) -> Conversations | None:
        pass

    @abstractmethod
    async def insert_new_conversation(
        self,
        customer_id: UUID,
    ) -> Conversations:
        pass

    @abstractmethod
    async def get_or_create_conversation(
        self,
        business_id: UUID | None,
        agent_id: UUID,
        customer_id: UUID,
    ) -> Conversations:
        pass

    @abstractmethod
    async def get_all_conversations_by_business_id(
        self, business_id: UUID
    ) -> list[Conversations] | None:
        pass

    @abstractmethod
    async def get_paginated_conversations_by_business_id(
        self, business_id: UUID, limit: int, offset: int
    ) -> tuple[list[dict], int]:
        """Returns (conversations_with_last_message, total_count)"""
        pass

    @abstractmethod
    async def update_conversation_status(
        self, conversation_id: UUID, need_human: bool
    ) -> Conversations | None:
        pass
