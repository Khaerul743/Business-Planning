from pydantic import BaseModel, Field

class ReviewHumanHandoffInput(BaseModel):
    handoff_reason: str = Field(description="Alasan kamu melakukan handoff kepada admin manusia", max_length=150)
    decision_summary: str = Field(description="Ringkasan dari keputusan yang kamu lakukan")
    conversation_summary: str = Field(description="Ringkasan dari conversation yang sedang dilakukan")

class JudgeDecision(BaseModel):
    handoff: bool = Field(
        description="Whether the conversation should be handed off to a human."
    )

    confidence: float = Field(
        ge=0,
        le=100,
        description="Confidence level of the decision."
    )

    justification: str = Field(
        description="A brief justification for the decision."
    )
    
    recommendation: str | None = Field(
        default=None,
        description=(
            "A recommendation for the Main Agent when handoff is not required. "
            "If appropriate, recommend using get_business_knowledge() and specify "
            "the most relevant business knowledge topic to search."
        ),
    )