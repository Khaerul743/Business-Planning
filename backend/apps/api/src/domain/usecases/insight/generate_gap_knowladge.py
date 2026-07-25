import httpx
from uuid import UUID, uuid4
from typing import Optional
from dataclasses import dataclass
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAnalyticRepository,
    IBusinessRepository,
    IInsightRepository,
)
from src.core.exceptions.business_exception import BusinessNotFound
from src.app.validators.insight_schema import AddGapKnowlage
from src.infrastructure.langgraph_server import langgraph_client, GapAnalysisAgentConfig

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

        super().__init__(__name__)

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

            # get conversation gap
            gap_conversation = await self.analytic_repo.get_knowladge_gap(
                input_data.agent_id
            )

            print("=========================")
            print(gap_conversation)

            if gap_conversation is None:
                return UseCaseResult.success_result(GenerateGapKnowladgeOutput())
            
            thread_id = uuid4()
            try:
                result = await langgraph_client.run_gap_analysis_agent(str(thread_id), GapAnalysisAgentConfig(str(input_data.agent_id),str(input_data.business_id), business.description, gap_conversation))
            except httpx.HTTPStatusError as exc:
                self.logger.error(f"Error run business insight agent: {exc}")
                self.logger.info("Registered new thread id by business id")
                await langgraph_client.register_thread_id(thread_id)
                self.logger.info("Re-run business insight agent")
                result = await langgraph_client.run_gap_analysis_agent(str(thread_id), GapAnalysisAgentConfig(str(input_data.agent_id),str(input_data.business_id), business.description, gap_conversation))

            print(result)
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
            self.logger.error(f"Error while generate gap knowladge: {e}")
            return UseCaseResult.error_result(
                f"Unexpected error in usecase Generate gap knowladge: {e}", e
            )
