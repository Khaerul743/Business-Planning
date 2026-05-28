# MASIH BELUM KEPAKE YGY
from dataclasses import dataclass
from uuid import UUID

from src.core.exceptions.agent_exception import AgentNotFound
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAgentRepository, ICustomerRepository


@dataclass
class CheckStatusAgentInput:
    agent_id: UUID


@dataclass
class CheckStatusAgentOutput:
    is_active: bool


class CheckStatusAgentUseCase(
    BaseUseCase[CheckStatusAgentInput, CheckStatusAgentOutput]
):
    def __init__(
        self, agent_repo: IAgentRepository, customer_repo: ICustomerRepository
    ):
        self.agent_repo = agent_repo
        self.customer_repo = customer_repo

    async def execute(
        self, input_data: CheckStatusAgentInput
    ) -> UseCaseResult[CheckStatusAgentOutput]:
        try:
            agent_status = await self.agent_repo.get_status_agent(input_data.agent_id)
            customer_status_agent = (
                await self.customer_repo.get_customer_status_agent_by_agent_id(
                    input_data.agent_id
                )
            )

            if agent_status is None:
                return UseCaseResult.error_result("Agent not found", AgentNotFound())
            elif customer_status_agent is None:
                return UseCaseResult.error_result(
                    "Customer not found", RuntimeWarning("Customer Not found")
                )

            if not agent_status or not customer_status_agent:
                return UseCaseResult.success_result(
                    CheckStatusAgentOutput(is_active=False)
                )

            return UseCaseResult.success_result(CheckStatusAgentOutput(is_active=True))

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while checking agent status: {e}", e
            )
