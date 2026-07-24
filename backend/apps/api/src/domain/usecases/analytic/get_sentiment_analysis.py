from dataclasses import dataclass
from uuid import UUID

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository


@dataclass
class GetSentimentAnalysisInput:
    agent_id: UUID


@dataclass
class GetSentimentAnalysisOutput:
    summary: dict[str, int]
    samples: dict[str, str | None]


class GetSentimentAnalysisUseCase(
    BaseUseCase[GetSentimentAnalysisInput, GetSentimentAnalysisOutput]
):
    def __init__(self, analytic_repo: IAnalyticRepository):
        self.analytic_repo = analytic_repo

    async def execute(
        self, input_data: GetSentimentAnalysisInput
    ) -> UseCaseResult[GetSentimentAnalysisOutput]:
        try:
            result = await self.analytic_repo.get_sentiment_analysis(input_data.agent_id)
            empty_summary = {"positif": 0, "netral": 0, "negatif": 0, "total": 0}
            empty_samples = {"positif": None, "netral": None, "negatif": None}

            if result is None or len(result) == 0:
                return UseCaseResult.success_result(
                    GetSentimentAnalysisOutput(summary=empty_summary, samples=empty_samples)
                )

            summary = {"positif": 0, "netral": 0, "negatif": 0, "total": 0}
            samples: dict[str, str | None] = {"positif": None, "netral": None, "negatif": None}

            for item in result:
                sentiment = item.get("sentiment", "netral")
                if sentiment not in ["positif", "netral", "negatif"]:
                    sentiment = "netral"

                summary[sentiment] += 1
                summary["total"] += 1

                user_message = item.get("user_message")
                if samples[sentiment] is None and user_message:
                    samples[sentiment] = user_message

            return UseCaseResult.success_result(
                GetSentimentAnalysisOutput(summary=summary, samples=samples)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting sentiment analysis: {e}", e
            )
