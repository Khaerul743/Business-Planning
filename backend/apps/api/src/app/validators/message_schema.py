from typing import Any, Literal, Optional

from pydantic import BaseModel


class InsertNewMessage(BaseModel):
    sender_type: Literal["ai", "customer", "human_admin"]
    message_type: Literal["text", "image", "audio", "file"]
    content: str
    raw_webhook: Optional[dict[str, Any]] = {}


class InsertDirectMessage(BaseModel):
    text_message: str
