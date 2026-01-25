from typing import Optional

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    object: str
    entry: list


class FilteredPayload(BaseModel):
    phone_number_id: str
    wa_id: Optional[str] = None
    name: Optional[str] = None
    from_number: Optional[str] = None
    message_type: Optional[str] = None
    text: Optional[str] = None
