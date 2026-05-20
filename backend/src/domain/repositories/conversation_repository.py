from typing import Literal
from uuid import UUID

from supabase import AsyncClient

from src.domain.models import Conversations
from src.domain.usecases.interfaces import IConversationRepository


class ConversationRepository(IConversationRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_conversation_by_id(
        self, conversation_id: UUID
    ) -> Conversations | None:
        result = (
            await self.db.table("Conversations")
            .select("*")
            .eq("id", conversation_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            return None

        return Conversations.model_validate(result.data)

    async def insert_new_conversation(
        self,
        customer_id: UUID,
    ) -> Conversations:
        payload = {"customer_id": str(customer_id)}
        result = await self.db.table("Conversations").insert(payload).execute()

        return Conversations.model_validate(result.data[0])

    async def get_or_create_conversation(
        self,
        business_id: UUID | None,
        agent_id: UUID,
        customer_id: UUID,
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
                "business_id": str(business_id),
                "agent_id": str(agent_id),
                "customer_id": str(customer_id),
            }
            result = await self.db.table("Conversations").insert(payload).execute()

            return Conversations.model_validate(result.data[0])

        return Conversations.model_validate(result.data)

    async def get_all_conversations_by_business_id(
        self, business_id: UUID
    ) -> list[dict] | None:
        result = (
            await self.db.table("Conversations")
            .select("*, Customers(name, phone_number)")
            .eq("business_id", business_id)
            .execute()
        )

        if len(result.data) == 0:
            return None

        list_conversations = []

        for i in result.data:
            i["username"] = i["Customers"]["name"]
            i["phone_number"] = i["Customers"]["phone_number"]
            del i["Customers"]

            list_conversations.append(i)

        return list_conversations

    async def get_paginated_conversations_by_business_id(
        self, business_id: UUID, limit: int, offset: int
    ) -> tuple[list[dict], int]:
        # Count total conversations
        count_result = (
            await self.db.table("Conversations")
            .select("id", count="exact")
            .eq("business_id", business_id)
            .execute()
        )
        total_count = count_result.count or 0

        if total_count == 0:
            return [], 0

        # Fetch paginated conversations with customer info
        result = (
            await self.db.table("Conversations")
            .select("*, Customers(name, phone_number)")
            .eq("business_id", business_id)
            .order("last_message_at", desc=True)
            .range(offset, offset + limit - 1)
            .execute()
        )

        conversations = []
        for row in result.data:
            row["username"] = row["Customers"]["name"]
            row["phone_number"] = row["Customers"]["phone_number"]
            del row["Customers"]

            # Fetch last message for this conversation
            last_msg_result = (
                await self.db.table("Messages")
                .select("content, sender_type, created_at")
                .eq("conversation_id", row["id"])
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            row["last_message"] = (
                last_msg_result.data[0] if last_msg_result.data else None
            )

            conversations.append(row)

        return conversations, total_count

    async def update_conversation_status(
        self, conversation_id: UUID, need_human: bool
    ) -> Conversations | None:
        result = (
            await self.db.table("Conversations")
            .update({"need_human": need_human})
            .eq("id", conversation_id)
            .execute()
        )
        if len(result.data) == 0:
            return None

        return Conversations.model_validate(result.data[0])
