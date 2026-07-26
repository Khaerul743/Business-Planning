from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel

SessionStatus = str
WhatsappEventType = str

class WaSessionMetadata(BaseModel):
    phone_number: Optional[str] = None
    display_name: Optional[str] = None
    business_id: Optional[str] = None
    session_id: Optional[str] = None

class WaSessionData(BaseModel):
    business_id: str
    session_id: Optional[str] = None
    status: SessionStatus
    qr_code: Optional[str] = None
    metadata: Optional[WaSessionMetadata] = None

class WaSessionResponse(BaseModel):
    success: bool
    data: Optional[WaSessionData] = None
    error: Optional[Dict[str, Any]] = None

class WaSessionListResponse(BaseModel):
    success: bool
    data: List[WaSessionData] = []
    total: int = 0
    
class WaSessionDestroyData(BaseModel):
    business_id: str
    status: SessionStatus
    
class WaSessionDestroyResponse(BaseModel):
    success: bool
    data: Optional[WaSessionDestroyData] = None
    error: Optional[Dict[str, Any]] = None

class WaSendMessageData(BaseModel):
    status: str
    business_id: str
    to: str
    message_id: Optional[str] = None
    
class WaSendMessageResponse(BaseModel):
    success: bool
    data: Optional[WaSendMessageData] = None
    error: Optional[Dict[str, Any]] = None

# Websocket Schemas
class WhatsappEventPayload(BaseModel):
    """
    Schema for incoming events from the WA-Bridge Node.js service.
    These events will be broadcasted to the connected websockets.
    """
    event: WhatsappEventType
    business_id: str
    session_id: Optional[str] = None
    status: Optional[SessionStatus] = None
    qr_code: Optional[str] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None

class SaveChannelDataPayload(BaseModel):
    phone_number: str
    display_name: Optional[str] = None
    status: SessionStatus

