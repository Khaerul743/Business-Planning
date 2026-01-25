from datetime import datetime
from typing import Literal, Optional

from .base import BaseEntity


class Conversations(BaseEntity):
    customer_id: Optional[int] = None
    status: Literal["active", "inactive"] = "active"
    last_message_at: datetime
