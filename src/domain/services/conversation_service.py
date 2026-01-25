from supabase import AsyncClient

from src.core.context.request_context import current_user_id
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.repositories import (
    BusinessRepository,
    ConversationRepository,
    MessageRepository,
)

from .base import BaseService


class ConversationService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        # Repositories
        self.conversation_repo = ConversationRepository(db)
        self.business_repo = BusinessRepository(db)
        self.message_repo = MessageRepository(db)

    async def _get_business_id(self, user_id: int) -> int | None:
        business_id = await self.business_repo.get_business_id_by_user_id(user_id)
        return business_id

    async def get_all_conversation(self):
        user_id = current_user_id.get()
        if user_id is None:
            raise UnauthorizedException()

        business_id = await self._get_business_id(user_id)
        if business_id is None:
            raise BusinessNotFound()

        conversations = (
            await self.conversation_repo.get_all_conversations_by_business_id(
                business_id
            )
        )

        return conversations

    async def get_all_messages(self, conversation_id: int):
        messages = await self.message_repo.get_all_message_by_conversation_id(
            conversation_id
        )

        return messages
