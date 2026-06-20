from pydantic import BaseModel, Field

class HumanHandoffInput(BaseModel):
    confidence_level: float = Field(description="Tingkat kepercayaan diri kamu sekarang")
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
        max_length=150,
        description="A brief justification for the decision."
    )