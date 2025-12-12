from datetime import datetime
from typing import Optional

from .base import BaseModelSchema


class Business(BaseModelSchema):
    user_id: Optional[int] = None
    name: str
    owner_name: Optional[str] = None
    phone_number: str
    updated_at: datetime
