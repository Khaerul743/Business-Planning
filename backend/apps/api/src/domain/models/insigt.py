from uuid import UUID
from .base import BaseEntity


class Insight(BaseEntity):
    business_id: UUID
    overview: str
    insight: str
    reason: str
    impact: str
    recommendation: str
