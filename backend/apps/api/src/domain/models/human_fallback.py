from typing import Optional
from uuid import UUID

from .base import BaseEntity


class Human_Fallback(BaseEntity):
    business_id: Optional[UUID] = None
    conversation_id: Optional[UUID] = None
    confidence_level: float
    last_decision_summary: str
