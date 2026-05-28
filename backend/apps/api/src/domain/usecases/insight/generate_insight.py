from uuid import UUID
from dataclasses import dataclass
from src.infrastructure.ai.agent.agent_analysis_messages import (
    AgentAnalysisMessages,
    AgentAnalysisState,
)
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IInsightRepository, IBusinessRepository
from src.app.validators.insight_schema import AddInsight
from src.domain.models import Insight
from src.domain.usecases.analytic import (
    GetCategoryPercentages,
    GetCategoryPercentagesInput,
)
from src.core.exceptions.business_exception import BusinessNotFound


@dataclass
class GenerateInsightInput:
    business_id: UUID
    agent_id: UUID


@dataclass
class GenerateInsightOutput:
    insight: Insight


class GenerateInsight(BaseUseCase[GenerateInsightInput, GenerateInsightOutput]):
    def __init__(
        self,
        insight_repo: IInsightRepository,
        business_repo: IBusinessRepository,
        category_percentage_usecase: GetCategoryPercentages,
    ):
        self.insight_repo = insight_repo
        self.business_repo = business_repo
        self.category_percentage_usecase = category_percentage_usecase
        self.agent_analysis = AgentAnalysisMessages()

    async def execute(
        self, input_data: GenerateInsightInput
    ) -> UseCaseResult[GenerateInsightOutput]:
        try:
            category_percentage_result = await self.category_percentage_usecase.execute(
                GetCategoryPercentagesInput(input_data.agent_id, "weekly")
            )
            if not category_percentage_result.is_success():
                exception = category_percentage_result.get_exception()
                if exception:
                    return UseCaseResult.error_result(
                        "Category percentage usecase did not successfully.", exception
                    )
                else:
                    return UseCaseResult.error_result(
                        "Category percentage usecase did not successfully.",
                        RuntimeError(
                            "Category percentage usecase did not successfully."
                        ),
                    )

            result_data = category_percentage_result.get_data()
            if result_data is None:
                return UseCaseResult.error_result(
                    "Category percentage usecase did not successfully.",
                    RuntimeError("Category percentage usecase did not successfully."),
                )

            category_percentage = result_data.model_dump()

            # Get Business description
            business = await self.business_repo.get_business_by_id(
                input_data.business_id
            )
            if business is None:
                return UseCaseResult.error_result(
                    "Business not found", BusinessNotFound()
                )

            # Generate Insight
            result = self.agent_analysis.execute(
                AgentAnalysisState(
                    messages=[],
                    user_message="",
                    business_description=business.description,
                    raw_data=category_percentage,
                ),
                "default",
            )

            insight_payload = AddInsight(
                overview=result["insight_context"],
                insight=result["insight"],
                reason=result["reason"],
                impact=result["impact"],
                recommendation=result["recommendation"],
            )
            insight = await self.insight_repo.createInsight(
                input_data.business_id, insight_payload
            )

            return UseCaseResult.success_result(GenerateInsightOutput(insight=insight))
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error in generate insight usecase: {e}", e
            )
