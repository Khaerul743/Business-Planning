from pydantic import BaseModel, Field

class HumanHandoffInput(BaseModel):
    confidence_level: float = Field(description="Tingkat kepercayaan diri kamu sekarang", default=50)
    handoff_reason: str = Field(description="Alasan kamu melakukan handoff kepada admin manusia", max_length=150)
    decision_summary: str = Field(description="Ringkasan dari keputusan yang kamu lakukan")