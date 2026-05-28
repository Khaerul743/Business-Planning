from dataclasses import dataclass
from uuid import UUID

from src.core.exceptions.agent_exception import (
    AgentConfigurationNotFound,
    AgentNotFound,
)
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAgentConfigurationRepository,
    IAgentRepository,
)


@dataclass
class GetAgentInput:
    agent_id: UUID


@dataclass
class GetAgentOutput:
    result_data: dict


class GetAgentUseCase(BaseUseCase[GetAgentInput, GetAgentOutput]):
    def __init__(
        self,
        agent_repo: IAgentRepository,
        agent_conf_repo: IAgentConfigurationRepository,
    ):
        self.agent_repo = agent_repo
        self.agent_conf_repo = agent_conf_repo

    async def execute(self, input_data: GetAgentInput) -> UseCaseResult[GetAgentOutput]:
        try:
            agent = await self.agent_repo.get_agent_by_id(input_data.agent_id)
            if agent is None:
                return UseCaseResult.error_result("Agent not found", AgentNotFound())

            agent_conf = await self.agent_conf_repo.get_agent_conf_by_agent_id(
                input_data.agent_id
            )
            if agent_conf is None:
                return UseCaseResult.error_result(
                    "Agent conf not found", AgentConfigurationNotFound()
                )

            agent_detail = {
                "id": agent.id,
                "name": agent.name,
                "enable_ai": agent.enable_ai,
                "phone_number_id": agent.phone_number_id,
                "fallback_email": agent_conf.fallback_email,
                "base_prompt": agent_conf.base_prompt,
                "llm_model": agent_conf.llm_model,
                "llm_provider": agent_conf.llm_provider,
                "tone": agent_conf.tone,
                "temperature": agent_conf.temperature,
                "created_at": agent.created_at,
                "updated_at": agent.updated_at,
            }

            return UseCaseResult.success_result(
                GetAgentOutput(result_data=agent_detail)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting agent: {e}", e
            )
