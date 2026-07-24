from datetime import datetime
from uuid import UUID

from supabase import AsyncClient

from src.app.validators.analytic_schema import InsertAgentAnalytic
from src.domain.models import AgentAnalytics
from src.domain.usecases.interfaces import IAnalyticRepository


class AnalyticsRepository(IAnalyticRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_agent_analytics(self, agent_id: UUID):
        result = (
            await self.db.table("Agent_analytics")
            .select("*")
            .eq("agent_id", agent_id)
            .execute()
        )
        if len(result.data) == 0:
            return None

        result_data = [AgentAnalytics.model_validate(i) for i in result.data]
        return result_data

    async def insert_agent_analytic(
        self, agent_id: UUID, payload: InsertAgentAnalytic
    ) -> AgentAnalytics:
        payload_dict = payload.model_dump(exclude_unset=True)
        payload_dict["agent_id"] = str(agent_id)
        result = await self.db.table("Agent_analytics").insert(payload_dict).execute()
        return AgentAnalytics.model_validate(result.data[0])

    async def get_token_usage_trend(self, agent_id: UUID) -> list[dict] | None:
        result = (
            await self.db.table("Agent_analytics")
            .select("date, token")
            .eq("agent_id", agent_id)
            .execute()
        )
        if len(result.data) == 0:
            return None

        return result.data

    async def get_message_usage_trend(self, agent_id: UUID) -> list[dict] | None:
        result = (
            await self.db.table("Agent_analytics")
            .select("date, total_message")
            .eq("agent_id", agent_id)
            .execute()
        )
        if len(result.data) == 0:
            return None

        return result.data

    async def get_human_vs_ai_message_trend(
        self,
        agent_id: UUID,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[dict] | None:
        try:
            # Step 1: Get conversation IDs for the agent
            conversations = (
                await self.db.table("Conversations")
                .select("id, Customers!inner(agent_id)")
                .eq("Customers.agent_id", agent_id)
                .execute()
            )

            conversation_ids = [item["id"] for item in conversations.data]

            if not conversation_ids:
                return None

            # Step 2: Fetch messages for these conversations
            query = (
                self.db.table("Messages")
                .select("created_at, sender_type")
                .in_("conversation_id", conversation_ids)
            )

            if since is not None:
                query = query.gte("created_at", since.isoformat())
            if until is not None:
                query = query.lte("created_at", until.isoformat())

            messages = await query.execute()

            if len(messages.data) == 0:
                return None

            return messages.data

        except Exception as e:
            print(f"Error fetching human vs ai trend: {e}")
            return None

    async def get_category_messages(
        self,
        agent_id: UUID,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[dict] | None:
        try:
            query = (
                self.db.table("Agent_analytics")
                .select("category, user_message")
                .eq("agent_id", str(agent_id))
            )

            if since is not None:
                query = query.gte("date", since.isoformat())

            if until is not None:
                query = query.lte("date", until.isoformat())

            result = await query.execute()

            if len(result.data) == 0:
                return None

            return result.data

        except Exception as e:
            print(f"Error fetching category messages: {e}")
            return None

    async def get_knowladge_gap(self, agent_id: UUID) -> None | list[dict]:
        # Pastikan agent_id di-convert ke string kalau library-nya minta format str
        result = await self.db.rpc(
            "get_random_gap_knowladge",
            {
                "params": {
                    "p_limit_num": 5,
                    "p_agent_id": "a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58",
                }
            },
        ).execute()

        # Cek apakah result.data ada isinya
        if not result.data:
            return None

        return result.data

    async def get_sentiment_analysis(
        self,
        agent_id: UUID,
        since: datetime | None = None,
        until: datetime | None = None,
    ) -> list[dict] | None:
        try:
            query = (
                self.db.table("Agent_analytics")
                .select("sentiment, user_message")
                .eq("agent_id", str(agent_id))
            )

            if since is not None:
                query = query.gte("date", since.isoformat())

            if until is not None:
                query = query.lte("date", until.isoformat())

            result = await query.execute()

            if len(result.data) == 0:
                return None

            return result.data

        except Exception as e:
            print(f"Error fetching sentiment analysis: {e}")
            return None

