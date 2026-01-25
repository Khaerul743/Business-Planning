from supabase import AsyncClient

from src.app.validators.message_schema import InsertNewMessage
from src.domain.models import Messages
from src.domain.usecases.interfaces import IMessageRepository


class MessageRepository(IMessageRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def insert_new_message(
        self, conversation_id: int, message_data: InsertNewMessage
    ) -> Messages:
        payload = message_data.model_dump()
        payload["conversation_id"] = conversation_id
        result = await self.db.table("Messages").insert(payload).execute()
        return Messages.model_validate(result.data[0])

    async def get_all_message_by_conversation_id(
        self, conversation_id: int
    ) -> list[Messages] | None:
        result = (
            await self.db.table("Messages")
            .select("*")
            .eq("conversation_id", conversation_id)
            .order("created_at")
            .execute()
        )
        if len(result.data) == 0:
            return None
        messages = [Messages.model_validate(i) for i in result.data]
        return messages
