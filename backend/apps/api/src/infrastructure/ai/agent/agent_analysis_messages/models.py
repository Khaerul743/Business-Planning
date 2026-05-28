from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from src.infrastructure.ai.agent.base import BaseAgentStateModel


class InsightGeneratorOutput(BaseModel):
    insight: str = Field(
        description="A clear and concise summary of the most important pattern or issue observed from the data."
    )
    reason: str = Field(
        description="Explanation of why the insight is happening, based only on the provided context and customer messages."
    )
    impact: str = Field(
        description="The potential effect of this insight on the business, such as customer experience, revenue, or operations."
    )


class AgentAnalysisState(BaseAgentStateModel):
    business_description: str
    raw_data: dict
    insight_context: Optional[str] = None
    insight: Optional[str] = None
    reason: Optional[str] = None
    impact: Optional[str] = None
    recommendation: Optional[str] = None
