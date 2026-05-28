from uuid import UUID

from supabase import AsyncClient
from src.app.validators.insight_schema import AddGapKnowlage
from src.domain.models import GapKnowladge
from src.app.validators.insight_schema import AddInsight
from src.domain.usecases.interfaces import IInsightRepository
from src.domain.models import Insight


class InsightRepository(IInsightRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def createInsight(self, business_id: UUID, payload: AddInsight) -> Insight:
        payload_dict = payload.model_dump()
        payload_dict["business_id"] = str(business_id)
        result = await self.db.table("Insight").insert(payload_dict).execute()
        result_data = result.data[0]
        return Insight.model_validate(result_data)

    async def get_current_insight(self, business_id: UUID) -> None | Insight:
        result = (
            await self.db.table("Insight")
            .select("*")
            .eq("business_id", str(business_id))
            .order("created_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None
        return Insight.model_validate(result.data)

    async def get_current_gap(self, business_id: UUID) -> None | GapKnowladge:
        result = (
            await self.db.table("Gap_knowladge")
            .select("*")
            .eq("business_id", str(business_id))
            .order("created_at", desc=True)
            .limit(1)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None
        return GapKnowladge.model_validate(result.data)

    async def insert_gap_knowladge(
        self, business_id: UUID, payload: AddGapKnowlage
    ) -> GapKnowladge:
        payload_dict = payload.model_dump()
        payload_dict["business_id"] = business_id
        result = await self.db.table("Gap_knowladge").insert(payload_dict).execute()
        result_data = result.data[0]
        return GapKnowladge.validate(result_data)
