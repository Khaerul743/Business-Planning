from typing import Optional
from uuid import UUID

from .base import BaseEntity


class Customers(BaseEntity):
    agent_id: Optional[UUID] = None
    wa_id: str
    name: str
    phone_number: str
    enable_ai: bool = True
