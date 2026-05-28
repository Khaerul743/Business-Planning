from datetime import datetime
from typing import Literal, Optional
from uuid import UUID

from .base import BaseEntity


class Messages(BaseEntity):
    conversation_id: Optional[UUID] = None
    message_type: Literal["text", "image", "audio", "file"] = "text"
    content: str
    raw_webhook: Optional[dict] = {}
    sender_type: Literal["ai", "customer", "human_admin"]
