from typing import Literal

from supabase import AsyncClient

from src.domain.models import Conversations
from src.domain.usecases.interfaces import IConversationRepository


class ConversationRepository(IConversationRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def insert_new_conversation(
        self,
        customer_id: int,
        status: Literal["active"] | Literal["inactive"] = "active",
    ) -> Conversations:
        payload = {"customer_id": customer_id, "status": status}
        result = await self.db.table("Conversations").insert(payload).execute()

        return Conversations.model_validate(result.data[0])

    async def get_or_create_conversation(
        self,
        business_id: int | None,
        agent_id: int,
        customer_id: int,
        status: Literal["active"] | Literal["inactive"] = "active",
    ) -> Conversations:
        result = await (
            self.db.table("Conversations")
            .select("*")
            .eq("customer_id", customer_id)
            .eq("agent_id", agent_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            payload = {
                "business_id": business_id,
                "agent_id": agent_id,
                "customer_id": customer_id,
                "status": status,
            }
            result = await self.db.table("Conversations").insert(payload).execute()

            return Conversations.model_validate(result.data[0])

        return Conversations.model_validate(result.data)

    async def get_all_conversations_by_business_id(
        self, business_id: int
    ) -> list[dict] | None:
        result = (
            await self.db.table("Conversations")
            .select("*, Customers(name)")
            .eq("business_id", business_id)
            .execute()
        )

        if len(result.data) == 0:
            return None

        list_conversations = []

        for i in result.data:
            i["username"] = i["Customers"]["name"]
            del i["Customers"]

            list_conversations.append(i)

        return list_conversations
