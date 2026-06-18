from uuid import UUID
from supabase import AsyncClient
from src.repositories.knowladge_repository import KnowladgeRepository
from shared.schemas import AgentConfig
from shared.utils.logger import get_logger


class AgentConfigurationManager:
    def __init__(self, db: AsyncClient):
        self.knowladge_repo = KnowladgeRepository(db)
        self.cache: dict[str, AgentConfig] = {}
        self._logger = get_logger(__name__)

    async def _get_agent_configuration(self, agent_id: UUID) -> AgentConfig | None:
        agent_conf = await self.knowladge_repo.get_agent_conf_by_agent_id(agent_id)
        if agent_conf is None:
            self._logger.warning(
                f"Agent configuration not found: agent id {str(agent_id)}"
            )
            return

        agent_config = AgentConfig(
            chromadb_path=agent_conf.chromadb_path,
            collection_name=agent_conf.collection_name,
            llm_model=agent_conf.llm_model,
            llm_provider=agent_conf.llm_provider,
            tone=agent_conf.tone,
            base_prompt=agent_conf.base_prompt,
            temperature=agent_conf.temperature,
        )

        return agent_config

    async def get(self, agent_id: UUID):
        agent_config = self.cache.get(str(agent_id), None)
        if agent_config is None:
            agent_config = await self._get_agent_configuration(agent_id)
            if agent_config is None:
                raise RuntimeError("Agent configuration not found")

            self.cache[str(agent_id)] = agent_config
        return agent_config
