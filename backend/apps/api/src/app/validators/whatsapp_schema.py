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
    message_id: Optional[str] = None
    is_from_wa_service: bool = False

class SendMessagePayload(BaseModel):
    business_id: str
    to: str
    message:str