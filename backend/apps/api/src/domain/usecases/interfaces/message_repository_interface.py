from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.message_schema import InsertNewMessage
from src.domain.models import Messages


class IMessageRepository(ABC):
    @abstractmethod
    async def get_all_message_by_conversation_id(
        self, conversation_id: UUID
    ) -> list[Messages] | None:
        pass

    @abstractmethod
    async def insert_new_message(
        self, conversation_id: UUID, message_data: InsertNewMessage
    ) -> Messages:
        pass
