from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel


class InsertAgentAnalytic(BaseModel):
    date: str
    total_message: int
    human_takeover: Optional[int] = 0
    response_time: float
    token: int
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
    ] = "lainnya"
    ai_response: str
    is_business_related: bool
    knowledge_gap_detected: bool
    created_at: Optional[datetime] = None
