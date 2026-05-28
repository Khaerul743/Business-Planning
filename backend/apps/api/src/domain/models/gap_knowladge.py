from uuid import UUID
from .base import BaseEntity


class GapKnowladge(BaseEntity):
    business_id: UUID
    insight: str
    knowladge_business_gap: str
    recommendation: str
