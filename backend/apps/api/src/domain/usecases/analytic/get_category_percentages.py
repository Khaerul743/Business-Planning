from dataclasses import dataclass
from uuid import UUID
from typing import Literal
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel
from collections import defaultdict
import random

from src.domain.usecases.base import UseCaseResult, BaseUseCase
from src.domain.usecases.interfaces import IAnalyticRepository

PeriodType = Literal["day", "weekly", "alltime"]


@dataclass
class GetCategoryPercentagesInput:
    agent_id: UUID
    period: PeriodType = "alltime"


class SummaryType(BaseModel):
    category_type: Literal[
        "pengiriman",
        "harga",
        "promo",
        "produk",
        "stok",
        "pemesanan",
        "komplain",
        "refund",
        "lainnya",
    ]
    total: int
    change: str  # e.g. "+12.50%", "-5.00%", "N/A"


class SampleType(BaseModel):
    category_type: Literal[
        "pengiriman",
        "harga",
        "promo",
        "produk",
        "stok",
        "pemesanan",
        "komplain",
        "refund",
        "lainnya",
    ]
    sample_messages: list[str]


class GetCategoryPercentagesOutput(BaseModel):
    summary: list[SummaryType]
    samples: list[SampleType]


def _count_by_category(data: list[dict]) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for row in data:
        cat = row.get("category", "lainnya")
        totals[cat] += 1
    return dict(totals)


def _format_change(current: int, previous: int) -> str:
    """Returns percentage change string: (current - previous) / previous * 100%"""
    if previous == 0:
        return "+100.00%" if current > 0 else "N/A"
    pct = (current - previous) / previous * 100
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.2f}%"


class GetCategoryPercentages(
    BaseUseCase[GetCategoryPercentagesInput, GetCategoryPercentagesOutput]
):
    def __init__(self, analytic_repo: IAnalyticRepository):
        self.analyic_repo = analytic_repo

    async def execute(
        self, input_data: GetCategoryPercentagesInput
    ) -> UseCaseResult[GetCategoryPercentagesOutput]:
        try:
            now = datetime.now(timezone.utc)

            # Determine current & previous period boundaries
            if input_data.period == "day":
                current_since = now - timedelta(days=1)
                current_until = now
                prev_since = now - timedelta(days=2)
                prev_until = current_since
            elif input_data.period == "weekly":
                current_since = now - timedelta(weeks=1)
                current_until = now
                prev_since = now - timedelta(weeks=2)
                prev_until = current_since
            else:
                # alltime: no previous period to compare
                current_since = None
                current_until = None
                prev_since = None
                prev_until = None

            # Fetch current period data
            current_data = await self.analyic_repo.get_category_messages(
                input_data.agent_id, since=current_since, until=current_until
            )

            if current_data is None or len(current_data) == 0:
                return UseCaseResult.success_result(
                    GetCategoryPercentagesOutput(summary=[], samples=[])
                )

            current_totals = _count_by_category(current_data)

            # Fetch previous period data (only when period is day or weekly)
            prev_totals: dict[str, int] = {}
            if prev_since is not None:
                prev_data = await self.analyic_repo.get_category_messages(
                    input_data.agent_id, since=prev_since, until=prev_until
                )
                if prev_data:
                    prev_totals = _count_by_category(prev_data)

            # Build summary with percentage change
            summary: list[SummaryType] = []
            for cat, total in current_totals.items():
                if input_data.period == "alltime":
                    change_str = "N/A"
                else:
                    prev_total = prev_totals.get(cat, 0)
                    change_str = _format_change(total, prev_total)

                summary.append(
                    SummaryType(
                        category_type=cat,
                        total=total,
                        change=change_str,
                    )
                )

            # Build samples list (3–5 random messages per category)
            category_messages: dict[str, list[str]] = defaultdict(list)
            for row in current_data:
                cat = row.get("category", "lainnya")
                msg = row.get("user_message", "")
                if msg:
                    category_messages[cat].append(msg)

            samples: list[SampleType] = []
            for cat, messages in category_messages.items():
                sample_count = min(5, len(messages))
                sample_count = max(sample_count, min(3, len(messages)))
                sampled = random.sample(messages, sample_count)
                samples.append(
                    SampleType(
                        category_type=cat,
                        sample_messages=sampled,
                    )
                )

            return UseCaseResult.success_result(
                GetCategoryPercentagesOutput(summary=summary, samples=samples)
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting category percentages: {e}", e
            )
