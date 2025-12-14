from datetime import datetime
from typing import Literal, Optional

from .base import BaseEntity


class BusinessKnowladge(BaseEntity):
    business_id: Optional[int] = None
    category: str
    description: str
    content: str
    format: Literal["text", "json", "markdown"] = "text"
    updated_at: datetime
