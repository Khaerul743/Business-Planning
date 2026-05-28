from datetime import datetime
from typing import Optional, Literal
from uuid import UUID

from .base import BaseEntity


class AgentAnalytics(BaseEntity):
    agent_id: UUID
    date: datetime
    total_message: int
    human_takeover: int
    response_time: float
    token: int
    ai_response: str
    user_message: str
    category: Literal[
        "pengiriman",
        "harga",
        "promo",
        "produk",
        "stok",
        "pemesanan",
        "komplain",
        "refund",
        "lainnya",
    ]
    knowledge_gap_detected: bool
    is_business_related: bool
