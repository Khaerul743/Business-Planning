from datetime import datetime
from typing import Literal, Optional

from .base import BaseEntity


class Conversations(BaseEntity):
    customer_id: Optional[str] = None
    status: Literal["active", "inactive"] = "active"
    last_message: datetime
