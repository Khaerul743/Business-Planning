from supabase import AsyncClient

from src.app.validators.agent_schema import AgentConf
from src.domain.models import Agent_configuration
from src.domain.usecases.interfaces import IAgentConfigurationRepository


class AgentConfigurationRepository(IAgentConfigurationRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_agent_conf_by_agent_id(
        self, agent_id: int
    ) -> Agent_configuration | None:
        result = (
            await self.db.table("Agent_configurations")
            .select("*")
            .eq("agent_id", agent_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            return None

        return Agent_configuration.model_validate(result.data)

    async def insert_agent_conf(
        self, agent_id: int, agent_conf: AgentConf
    ) -> Agent_configuration:
        payload = agent_conf.model_dump()
        payload["agent_id"] = agent_id
        print(payload)
        result = await self.db.table("Agent_configurations").insert(payload).execute()

        return Agent_configuration.model_validate(result.data[0])
