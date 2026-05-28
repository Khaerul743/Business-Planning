from uuid import UUID

from src.domain.services import ConversationService
from supabase import AsyncClient

from .base import BaseController


class ConversationController(BaseController):
    def __init__(self, db: AsyncClient):
        self.conversation_service = ConversationService(db)

    async def get_all_conversation_handler(self, page: int = 1, limit: int = 10):
        result = await self.conversation_service.get_all_conversation(
            page=page, limit=limit
        )
        return result

    async def get_all_messages_handler(self, conversation_id: UUID):
        messages = await self.conversation_service.get_all_messages(conversation_id)
        if messages is None:
            return []

        return messages

    async def get_all_conversation_human_fallback_handler(self):
        conversation_fallback = (
            await self.conversation_service.get_all_conversation_with_human_fallback()
        )

        return conversation_fallback

    async def get_conversation_fallback_handler(self, conversation_id: UUID):
        conversation_fallback = (
            await self.conversation_service.get_conversation_fallback(conversation_id)
        )
        conv_fallback_dict = conversation_fallback.model_dump()
        del conv_fallback_dict["business_id"]
        return conv_fallback_dict

    async def post_direct_message_handler(
        self, conversation_id: UUID, text_message: str
    ):
        result = await self.conversation_service.post_new_message(
            conversation_id, text_message
        )
        return {
            "conversation_id": result.conversation_id,
            "detail": result.response_webhook,
        }

    async def get_customer_status_agent_handler(self, conversation_id: UUID):
        result = await self.conversation_service.get_customer_status_agent(
            conversation_id
        )
        return {"customer_status_agent": result}

    async def update_customer_status_agent_handler(
        self, conversation_id: UUID, status: bool
    ):
        result = await self.conversation_service.update_customer_status_agent(
            conversation_id, status
        )
        return result.model_dump()

    async def delete_conversation_fallback_handler(self, conversation_id: UUID):
        result = await self.conversation_service.delete_conversation_fallback(
            conversation_id
        )
        return result.model_dump()
