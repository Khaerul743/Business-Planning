from datetime import datetime
from typing import Optional

from .base import BaseEntity


class Agents(BaseEntity):
    business_id: Optional[int] = None
    name: str
    llm_provider: str
    llm_model: str
    temperature: float = 0.7
    enable_ai: bool = True
    fallback_to_human: str
    updated_at: datetime
