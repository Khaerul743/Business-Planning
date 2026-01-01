from dataclasses import dataclass

from src.app.validators.agent_schema import CreateAgentIn, WhatsappAgentConfig
from src.domain.models import Agents
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAgentRepository
from src.infrastructure.ai.agent.manager import WhatsappAgentManager


@dataclass
class CreateAgentUseCaseInput:
    business_id: int
    agent_data: CreateAgentIn


@dataclass
class CreateAgentUseCaseOutput:
    agent_data: Agents


class CreateAgentUseCase(
    BaseUseCase[CreateAgentUseCaseInput, CreateAgentUseCaseOutput]
):
    def __init__(
        self, agent_repo: IAgentRepository, agent_manager: WhatsappAgentManager
    ):
        self.agent_repo = agent_repo
        self.agent_manager = agent_manager

    async def execute(
        self, input_data: CreateAgentUseCaseInput
    ) -> UseCaseResult[CreateAgentUseCaseOutput]:
        try:
            # Create agent entity
            agent_entity = await self.agent_repo.create_agent_by_business_id(
                input_data.business_id, input_data.agent_data
            )

            # Agent configuration
            agent_conf = WhatsappAgentConfig(
                chromadb_path="chromadb",
                collection_name="my_collection",
                llm_provider=agent_entity.llm_provider,
                llm_model=agent_entity.llm_model,
                tone="casual",
                base_prompt="",
            )

            # Add to agent manager
            self.agent_manager.get_or_create(input_data.business_id, agent_conf)

            return UseCaseResult.success_result(CreateAgentUseCaseOutput(agent_entity))

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while creating agent: {str(e)}", e
            )
