from typing import Optional

from .base import BaseEntity


class Customers(BaseEntity):
    agent_id: Optional[int] = None
    wa_id: str
    name: str
    phone_number: str
    enable_ai: bool = True
