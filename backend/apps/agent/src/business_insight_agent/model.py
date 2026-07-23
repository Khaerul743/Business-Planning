from typing import Optional
from pydantic import BaseModel, Field
from src.base.base_state import BaseAgentStateModel
from shared.schemas import AgentConfig


class TextContent(BaseModel):
    content: str = Field(description="Berisi text yang memiliki panjang maksimal 120 char", max_length=120)

class InsightGeneratorOutput(BaseModel):
    insight: list[TextContent] = Field(
        description="A clear and concise summary of the most important pattern or issue observed from the data."
    )
    reason: str = Field(
        description="Explanation of why the insight is happening, based only on the provided context and customer messages.", max_length=150
    )
    impact: list[TextContent] = Field(
        description="The potential effect of this insight on the business, such as customer experience, revenue, or operations."
    )

class RecommendationOutput(BaseModel):
    recommendation: list[TextContent] = Field(description="Berikan rekomendasi kepada bisnis.")

class BusinessInsightState(BaseAgentStateModel):
    business_description: str
    raw_data: dict
    insight_context: Optional[str] = None
    insight: Optional[list[TextContent]] = None
    reason: Optional[str] = None
    impact: Optional[list[TextContent]] = None
    recommendation: Optional[list[TextContent]] = None

    # Configuration
    configuration: Optional[AgentConfig] = None
