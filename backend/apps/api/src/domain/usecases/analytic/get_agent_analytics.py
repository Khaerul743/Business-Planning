from dataclasses import dataclass
from uuid import UUID

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository


@dataclass
class GetAgentAnalyticsInput:
    agent_id: UUID


@dataclass
class GetAgentAnalyticsOutput:
    total_tokens: int
    total_messages: int
    avg_response_time: float
    total_human_takeovers: int = 0
    response_rate: float = 100


class GetAgentAnalyticsUseCase(
    BaseUseCase[GetAgentAnalyticsInput, GetAgentAnalyticsOutput]
):
    def __init__(self, analtic_repo: IAnalyticRepository):
        self.analytic_repo = analtic_repo

    async def execute(
        self, input_data: GetAgentAnalyticsInput
    ) -> UseCaseResult[GetAgentAnalyticsOutput]:
        try:
            list_tokens = []
            list_response_time = []
            list_messages = []
            list_human_takeovers = []
            list_total_response = []

            analytic_data = await self.analytic_repo.get_agent_analytics(
                input_data.agent_id
            )
            if analytic_data is None:
                return UseCaseResult.success_result(
                    GetAgentAnalyticsOutput(
                        total_tokens=0,
                        total_messages=0,
                        total_human_takeovers=0,
                        avg_response_time=0,
                    )
                )

            for i in analytic_data:
                list_tokens.append(i.token)
                list_response_time.append(i.response_time)
                list_messages.append(i.total_message)
                if i.human_takeover:
                    list_human_takeovers.append(1)
                else:
                    list_total_response.append(1)

            total_tokens = sum(list_tokens)
            total_messages = sum(list_messages)
            total_human_takeovers = sum(list_human_takeovers)
            avg_response_time = sum(list_response_time) / len(list_response_time)
            response_rate = (sum(list_total_response) / len(analytic_data)) * 100

            return UseCaseResult.success_result(
                GetAgentAnalyticsOutput(
                    total_tokens=total_tokens,
                    total_messages=total_messages,
                    total_human_takeovers=total_human_takeovers,
                    avg_response_time=avg_response_time,
                    response_rate=response_rate,
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting agent analytics: {e}", e
            )
