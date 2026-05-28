from uuid import UUID

from supabase import AsyncClient

from src.app.validators.human_fallback_schema import InsertNewHumanFallback
from src.domain.models import Human_Fallback
from src.domain.usecases.interfaces import IHumanFallbackRepository


class HumanFallbackRepository(IHumanFallbackRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_all_human_fallback_by_business_id(
        self, business_id: UUID
    ) -> list[Human_Fallback] | None:
        result = (
            await self.db.table("Human_Fallback")
            .select("*")
            .eq("business_id", business_id)
            .execute()
        )

        if len(result.data) == 0:
            return None

        result_data = [
            Human_Fallback.model_validate(
                {
                    "id": i["id"],
                    "conversation_id": i["conversation_id"],
                    "confidence_level": i["confidence_level"],
                    "last_decision_summary": i["last_decision_summary"],
                    "created_at": i["created_at"],
                }
            )
            for i in result.data
        ]

        return result_data

    async def get_human_fallback_by_id(
        self, conversation_id: UUID
    ) -> Human_Fallback | None:
        result = (
            await self.db.table("Human_Fallback")
            .select("*")
            .eq("conversation_id", conversation_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None
        return Human_Fallback.model_validate(result.data)

    async def get_or_insert_new_human_fallback(
        self, payload: InsertNewHumanFallback
    ) -> Human_Fallback:
        payload_dict = payload.model_dump(mode="json")
        human_fallback = (
            await self.db.table("Human_Fallback")
            .select("*")
            .eq("conversation_id", payload.conversation_id)
            .maybe_single()
            .execute()
        )
        if human_fallback is None:
            result = (
                await self.db.table("Human_Fallback").insert(payload_dict).execute()
            )
            return Human_Fallback.model_validate(result.data[0])
        return Human_Fallback.model_validate(human_fallback.data)

    async def delete_human_fallback_by_conversation_id(
        self, conversation_id: UUID
    ) -> Human_Fallback | None:
        result = (
            await self.db.table("Human_Fallback")
            .delete()
            .eq("conversation_id", conversation_id)
            .execute()
        )

        if len(result.data) == 0:
            return None

        result_data = Human_Fallback.model_validate(
            {
                "id": result.data[0]["id"],
                "conversation_id": result.data[0]["conversation_id"],
                "confidence_level": result.data[0]["confidence_level"],
                "last_decision_summary": result.data[0]["last_decision_summary"],
                "created_at": result.data[0]["created_at"],
            }
        )

        return result_data
