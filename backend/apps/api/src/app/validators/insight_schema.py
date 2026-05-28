from pydantic import BaseModel


class AddInsight(BaseModel):
    overview: str
    insight: str
    reason: str
    impact: str
    recommendation: str


class AddGapKnowlage(BaseModel):
    insight: str
    knowladge_business_gap: str
    recommendation: str
