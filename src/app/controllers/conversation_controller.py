from supabase import AsyncClient

from src.domain.services import ConversationService

from .base import BaseController


class ConversationController(BaseController):
    def __init__(self, db: AsyncClient):
        self.conversation_service = ConversationService(db)

    async def get_all_conversation_handler(self):
        conversations = await self.conversation_service.get_all_conversation()
        if conversations is None:
            return []
        return conversations

    async def get_all_messages_handler(self, conversation_id: int):
        messages = await self.conversation_service.get_all_messages(conversation_id)
        if messages is None:
            return []

        return messages
