from typing import Optional
from pydantic import BaseModel, Field
from src.infrastructure.ai.agent.base import BaseAgentStateModel


class ContextBuilderStructuredOutput(BaseModel):
    is_gap_knowladge: bool = Field(
        description="Apakah ada gap knowladge dari history percakapan"
    )
    insight_context: Optional[str] = Field(
        description="Hasil deskripsi dari percakapan"
    )


class InsigtGeneratorStructuredOutput(BaseModel):
    insight: str = Field(description="Hasil dari analisis dan insight yang kamu dapat.")
    knowladge_business_gap: str = Field(
        description="Deskripsikan secara singkat kekurangan dari knowladge bisnis"
    )


class AgentAnalysisGapState(BaseAgentStateModel):
    business_description: str
    raw_data: list[dict]
    is_gap_knowladge: bool = False
    insight_context: Optional[str] = None
    insight: Optional[str] = None
    knowladge_business_gap: Optional[str] = None
    recommendation: Optional[str] = None
