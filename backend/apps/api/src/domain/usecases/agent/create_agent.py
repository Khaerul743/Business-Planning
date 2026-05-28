from dataclasses import dataclass
from uuid import UUID

from src.app.validators.agent_schema import AgentConf, CreateAgentIn, InsertAgent
from src.domain.models import Agents
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAgentConfigurationRepository,
    IAgentRepository,
    IBusinessRepository,
)
from src.infrastructure.ai.agent.manager import WhatsappAgentManager


@dataclass
class CreateAgentUseCaseInput:
    business_id: UUID
    agent_data: CreateAgentIn


@dataclass
class CreateAgentUseCaseOutput:
    agent_data: Agents


class CreateAgentUseCase(
    BaseUseCase[CreateAgentUseCaseInput, CreateAgentUseCaseOutput]
):
    def __init__(
        self,
        agent_repo: IAgentRepository,
        agent_conf_repo: IAgentConfigurationRepository,
    ):
        self.agent_repo = agent_repo
        self.agent_conf_repo = agent_conf_repo

    async def execute(
        self, input_data: CreateAgentUseCaseInput
    ) -> UseCaseResult[CreateAgentUseCaseOutput]:
        try:
            # Create agent entity
            agent_entity = await self.agent_repo.create_agent_by_business_id(
                input_data.business_id,
                InsertAgent(
                    name=input_data.agent_data.name,
                    enable_ai=input_data.agent_data.enable_ai,
                    fallback_to_human=input_data.agent_data.fallback_to_human,
                ),
            )

            # Agent configuration
            agent_conf = AgentConf(
                chromadb_path="chromadb",
                collection_name=f"agent_{agent_entity.id}",
                llm_provider=input_data.agent_data.llm_provider,
                llm_model=input_data.agent_data.llm_model,
                tone=input_data.agent_data.tone,
                base_prompt=input_data.agent_data.base_prompt,
                include_memory=input_data.agent_data.include_memory,
            )

            # Insert agent configuration
            await self.agent_conf_repo.insert_agent_conf(agent_entity.id, agent_conf)

            return UseCaseResult.success_result(CreateAgentUseCaseOutput(agent_entity))

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while creating agent: {str(e)}", e
            )
