from dataclasses import dataclass
from uuid import UUID

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository


@dataclass
class GetMessageUsageTrendInput:
    agent_id: UUID


@dataclass
class GetMessageUsageTrendOutput:
    trend_data: list[dict]


class GetMessageUsageTrendUseCase(
    BaseUseCase[GetMessageUsageTrendInput, GetMessageUsageTrendOutput]
):
    def __init__(self, analytic_repo: IAnalyticRepository):
        self.analytic_repo = analytic_repo

    async def execute(
        self, input_data: GetMessageUsageTrendInput
    ) -> UseCaseResult[GetMessageUsageTrendOutput]:
        try:
            result = await self.analytic_repo.get_message_usage_trend(
                input_data.agent_id
            )
            if result is None:
                return UseCaseResult.success_result(GetMessageUsageTrendOutput([]))

            grouped_data = {}
            for item in result:
                date = item["date"]
                if date not in grouped_data:
                    grouped_data[date] = 0
                grouped_data[date] += item["total_message"]

            trend_data = [
                {"date": date, "total_message": count}
                for date, count in grouped_data.items()
            ]
            # Sort by date
            trend_data.sort(key=lambda x: x["date"])

            return UseCaseResult.success_result(GetMessageUsageTrendOutput(trend_data))
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting message usage trend: {e}", e
            )
