from dataclasses import dataclass
from uuid import UUID
from datetime import datetime, timedelta, timezone

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository


@dataclass
class GetHumanVsAiMessageTrendInput:
    agent_id: UUID
    period: str = "weekly"


@dataclass
class GetHumanVsAiMessageTrendOutput:
    trend_data: list[dict]


class GetHumanVsAiMessageTrendUseCase(
    BaseUseCase[GetHumanVsAiMessageTrendInput, GetHumanVsAiMessageTrendOutput]
):
    def __init__(self, analytic_repo: IAnalyticRepository):
        self.analytic_repo = analytic_repo

    async def execute(
        self, input_data: GetHumanVsAiMessageTrendInput
    ) -> UseCaseResult[GetHumanVsAiMessageTrendOutput]:
        try:
            today_utc = datetime.now(timezone.utc)
            if input_data.period == "day":
                since = today_utc - timedelta(days=1)
                grouping = "hour"
            elif input_data.period == "monthly":
                since = today_utc - timedelta(days=30)
                grouping = "day"
            else:  # defauls to weekly for anything else
                since = today_utc - timedelta(days=7)
                grouping = "day"

            result = await self.analytic_repo.get_human_vs_ai_message_trend(
                input_data.agent_id, since=since
            )
            if result is None:
                return UseCaseResult.success_result(GetHumanVsAiMessageTrendOutput([]))

            grouped_data = {}
            for item in result:
                # Parse created_at
                raw_date = item["created_at"]
                if isinstance(raw_date, str):
                    try:
                        # Handle potential timezone offsets like +00:00
                        date_obj = datetime.fromisoformat(
                            raw_date.replace("Z", "+00:00")
                        )
                    except ValueError:
                        continue
                elif isinstance(raw_date, datetime):
                    date_obj = raw_date
                else:
                    continue

                if grouping == "hour":
                    date_str = date_obj.strftime("%Y-%m-%d %H:00")
                else:
                    date_str = date_obj.strftime("%Y-%m-%d")

                sender_type = item["sender_type"]

                if date_str not in grouped_data:
                    grouped_data[date_str] = {"human": 0, "ai": 0}

                if sender_type == "ai":
                    grouped_data[date_str]["ai"] += 1
                elif sender_type == "human_admin":
                    grouped_data[date_str]["human"] += 1

            trend_data = [
                {"date": date, "human": counts["human"], "ai": counts["ai"]}
                for date, counts in grouped_data.items()
            ]

            # Sort by date naturally
            trend_data.sort(key=lambda x: x["date"])

            return UseCaseResult.success_result(
                GetHumanVsAiMessageTrendOutput(trend_data)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting human vs ai message trend: {e}", e
            )
