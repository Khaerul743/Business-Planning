from typing import Optional
from pydantic import BaseModel, Field
from src.base.base_state import BaseAgentStateModel
from shared.schemas import AgentConfig

class ContextBuilderStructuredOutput(BaseModel):
    is_gap_knowladge: bool = Field(
        description="Apakah ada gap knowladge dari history percakapan",
    )
    insight_context: Optional[str] = Field(
        description="Hasil deskripsi dari percakapan"
    )

class InsigtGeneratorStructuredOutput(BaseModel):
    insight: str = Field(description="Hasil dari analisis dan insight yang kamu dapat.", max_length=150)
    knowladge_business_gap: str = Field(
        description="Deskripsikan secara singkat kekurangan dari knowladge bisnis", max_length=150
    )

class RecommendationOutput(BaseModel):
    recommendation: str = Field(description="Berikan rekomendasi yang sesuai untuk bisnis")

class AgentAnalysisGapState(BaseAgentStateModel):
    business_description: str
    raw_data: list[dict]
    is_gap_knowladge: bool = False
    insight_context: Optional[str] = None
    insight: Optional[str] = None
    knowladge_business_gap: Optional[str] = None
    recommendation: Optional[str] = None

    # Configuration
    configuration: Optional[AgentConfig] = None