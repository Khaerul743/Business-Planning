from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from .base import BaseEntity


class WhatsappChannel(BaseEntity):
    business_id: UUID
    phone_number: str
    display_name: Optional[str] = None
    status: str
    connected_at: Optional[datetime] = None
