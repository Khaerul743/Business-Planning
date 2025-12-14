from datetime import datetime

from .base import BaseEntity


class AgentAnalytics(BaseEntity):
    agent_id: int
    date: datetime
    total_message: int
    ai_response: str
    human_takeovers: int
    avarage_response_time: float
    total_tokens: int
