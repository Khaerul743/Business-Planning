from supabase import AsyncClient

from src.app.validators.agent_schema import CreateAgentIn
from src.domain.models import Agents
from src.domain.usecases.interfaces import IAgentRepository


class AgentRepository(IAgentRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_agent_id_by_user_id(self, user_id: int) -> int | None:
        result = (
            await self.db.table("Businesses")
            .select("Agents(id)")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return result.data["Agents"][0]["id"]

    async def create_agent_by_business_id(
        self, business_id: int, agent_data: CreateAgentIn
    ) -> Agents:
        payload = agent_data.model_dump()
        payload["business_id"] = business_id

        result = await self.db.table("Agents").insert(payload).execute()

        return Agents.model_validate(result.data[0])
