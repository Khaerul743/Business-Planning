from dataclasses import dataclass
from uuid import UUID

from src.app.validators.agent_schema import UpdateAgentIn
from src.core.exceptions.agent_exception import AgentNotFound
from src.domain.models import Agent_configuration
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAgentConfigurationRepository,
    IAgentRepository,
)
from src.infrastructure.ai.agent.manager import WhatsappAgentManager


@dataclass
class UpdateAgentInput:
    agent_id: UUID
    phone_number_id: str
    agent_data: UpdateAgentIn


@dataclass
class UpdateAgentOutput:
    result_data: dict


class UpdateAgentUseCase(BaseUseCase[UpdateAgentInput, UpdateAgentOutput]):
    def __init__(
        self,
        agent_repo: IAgentRepository,
        agent_conf_repo: IAgentConfigurationRepository,
        wa_agent_manager: WhatsappAgentManager,
    ):
        self.agent_repo = agent_repo
        self.agent_conf_repo = agent_conf_repo
        self.wa_agent_manager = wa_agent_manager

    async def execute(
        self, input_data: UpdateAgentInput
    ) -> UseCaseResult[UpdateAgentOutput]:
        try:
            data = input_data.agent_data.model_dump(exclude_unset=True)
            if input_data.agent_data.name and len(data) == 1:
                await self.agent_repo.update_name_agent(
                    input_data.agent_id, input_data.agent_data.name
                )
                return UseCaseResult.success_result(
                    UpdateAgentOutput({"name": data["name"]})
                )
            elif input_data.agent_data.name and len(data) > 1:
                await self.agent_repo.update_name_agent(
                    input_data.agent_id, input_data.agent_data.name
                )

            new_agent_conf = await self.agent_conf_repo.update_agent_conf(
                input_data.agent_id, input_data.agent_data
            )
            if new_agent_conf is None:
                return UseCaseResult.error_result("Agent not found", AgentNotFound())
            # Del agent obj for rebuilt new configuration
            self.wa_agent_manager.remove_agent_by_phone_number_id(
                input_data.phone_number_id
            )
            return UseCaseResult.success_result(
                UpdateAgentOutput(new_agent_conf.model_dump())
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while updating agent: {e}", e
            )
