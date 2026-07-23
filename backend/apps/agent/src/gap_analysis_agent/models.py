from typing import Optional
from pydantic import BaseModel, Field
from src.base.base_state import BaseAgentStateModel
from shared.schemas import AgentConfig

class ContextBuilderStructuredOutput(BaseModel):
    is_gap_knowladge: bool = Field(
        description="Apakah ada gap knowladge dari history percakapan"
    )
    insight_context: Optional[str] = Field(
        description="Hasil deskripsi dari percakapan"
    )


class TextContent(BaseModel):
    content: str = Field(description="Bagian teks hasil analisis yang dapat diparsing sebagai daftar atau elemen terstruktur.", max_length=150)

class InsigtGeneratorStructuredOutput(BaseModel):
    insight: list[TextContent] = Field(description="Hasil dari analisis dan insight yang kamu dapat.")
    knowladge_business_gap: list[TextContent] = Field(
        description="Deskripsikan secara singkat kekurangan dari knowladge bisnis"
    )

class RecommendationOutput(BaseModel):
    recommendation: list[TextContent] = Field(description="Berikan rekomendasi yang sesuai untuk bisnis")

class AgentAnalysisGapState(BaseAgentStateModel):
    business_description: str
    raw_data: list[dict]
    is_gap_knowladge: bool = False
    insight_context: Optional[str] = None
    insight: Optional[str | list[TextContent]] = None
    knowladge_business_gap: Optional[str | list[TextContent]] = None
    recommendation: Optional[str | list[TextContent]] = None

    # Configuration
    configuration: Optional[AgentConfig] = None