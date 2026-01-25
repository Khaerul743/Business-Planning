from typing import Any, Literal

from pydantic import BaseModel


class InsertNewMessage(BaseModel):
    sender_type: Literal["ai", "customer", "human_admin"]
    message_type: Literal["text", "image", "audio", "file"]
    content: str
    raw_webhook: dict[str, Any]
