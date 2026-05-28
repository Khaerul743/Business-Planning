from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository


@dataclass
class GetTokenUsageTrendInput:
    agent_id: UUID


@dataclass
class GetTokenUsageTrendOutput:
    trend_data: list[dict]


class GetTokenUsageTrendUseCase(
    BaseUseCase[GetTokenUsageTrendInput, GetTokenUsageTrendOutput]
):
    def __init__(self, analytic_repo: IAnalyticRepository):
        self.analytic_repo = analytic_repo

    async def execute(
        self, input_data: GetTokenUsageTrendInput
    ) -> UseCaseResult[GetTokenUsageTrendOutput]:
        try:
            result = await self.analytic_repo.get_token_usage_trend(input_data.agent_id)
            if result is None:
                return UseCaseResult.success_result(GetTokenUsageTrendOutput([]))

            grouped_data = {}
            for item in result:
                date = item["date"]
                if date not in grouped_data:
                    grouped_data[date] = 0
                grouped_data[date] += item["token"]

            trend_data = [
                {"date": date, "token": token} for date, token in grouped_data.items()
            ]
            # Sort by date
            trend_data.sort(key=lambda x: x["date"])

            return UseCaseResult.success_result(GetTokenUsageTrendOutput(trend_data))
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting token usage trend: {e}", e
            )
