from uuid import UUID
from typing import Optional
from dataclasses import dataclass
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAnalyticRepository,
    IBusinessRepository,
    IInsightRepository,
)
from src.core.exceptions.business_exception import BusinessNotFound
from src.infrastructure.ai.agent.agent_analysis_gap import (
    AgentAnalysisGap,
    AgentAnalysisGapState,
)
from src.app.validators.insight_schema import AddGapKnowlage


@dataclass
class GenerateGapKnowladgeInput:
    business_id: UUID
    agent_id: UUID


@dataclass
class GenerateGapKnowladgeOutput:
    insight: Optional[str] = None
    knowladge_business_gap: Optional[str] = None
    recommendation: Optional[str] = None


class GenerateGapKnowladge(
    BaseUseCase[GenerateGapKnowladgeInput, GenerateGapKnowladgeOutput]
):
    def __init__(
        self,
        business_repo: IBusinessRepository,
        analytic_repo: IAnalyticRepository,
        insight_repo: IInsightRepository,
    ):
        self.business_repo = business_repo
        self.analytic_repo = analytic_repo
        self.insight_repo = insight_repo
        self.agent_analysis_gap = AgentAnalysisGap()

    async def execute(
        self, input_data: GenerateGapKnowladgeInput
    ) -> UseCaseResult[GenerateGapKnowladgeOutput]:
        try:
            # Get business description
            business = await self.business_repo.get_business_by_id(
                input_data.business_id
            )
            if business is None:
                return UseCaseResult.error_result(
                    "Business not found", BusinessNotFound()
                )
            business_description = business.description

            # get conversation gap
            gap_conversation = await self.analytic_repo.get_knowladge_gap(
                input_data.agent_id
            )
            if gap_conversation is None:
                return UseCaseResult.success_result(GenerateGapKnowladgeOutput())

            result = self.agent_analysis_gap.execute(
                AgentAnalysisGapState(
                    messages=[],
                    user_message="",
                    business_description=business_description,
                    raw_data=gap_conversation,
                ),
                thread_id="default",
            )

            # Insert into database
            result_db = await self.insight_repo.insert_gap_knowladge(
                input_data.business_id,
                AddGapKnowlage(
                    insight=result["insight"],
                    knowladge_business_gap=result["knowladge_business_gap"],
                    recommendation=result["recommendation"],
                ),
            )

            return UseCaseResult.success_result(
                GenerateGapKnowladgeOutput(
                    insight=result["insight"],
                    knowladge_business_gap=result["knowladge_business_gap"],
                    recommendation=result["recommendation"],
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error in usecase Generate gap knowladge: {e}", e
            )
