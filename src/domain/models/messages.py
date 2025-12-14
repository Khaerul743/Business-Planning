from datetime import datetime
from typing import Literal, Optional

from .base import BaseEntity


class Messages(BaseEntity):
    conversation_id: Optional[int] = None
    message_type: Literal["text", "image", "audio", "file"] = "text"
    content: str
    raw_webhook: str
    sender_type: Literal["ai", "customer", "human_admin"]
