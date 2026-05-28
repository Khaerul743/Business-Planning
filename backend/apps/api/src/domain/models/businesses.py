from datetime import datetime
from typing import Optional
from uuid import UUID

from .base import BaseEntity


class Business(BaseEntity):
    user_id: Optional[UUID] = None
    name: str
    owner_name: Optional[str] = None
    phone_number: str
    description: str
    address: str
    updated_at: datetime
