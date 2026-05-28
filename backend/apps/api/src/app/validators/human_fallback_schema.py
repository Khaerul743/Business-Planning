from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class InsertNewHumanFallback(BaseModel):
    business_id: UUID
    conversation_id: UUID
    confidence_level: float
    last_decision_summary: str
