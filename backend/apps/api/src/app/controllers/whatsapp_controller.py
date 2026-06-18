from supabase import AsyncClient

from src.app.validators.whatsapp_schema import WebhookPayload, SendMessagePayload
from src.app.validators.wa_service_schema import SaveChannelDataPayload
from src.domain.services import WhatsappService

from .base import BaseController


class WhatsappController(BaseController):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)
        self.whatsapp_service = WhatsappService(db)

    async def send_message(self, payload: WebhookPayload):
        if payload.object != "whatsapp_business_account":
            return {"status": "receive"}

        result = await self.whatsapp_service.send_text_message(payload)
        return result

    async def create_session_controller(self, business_id:str):
        result = await self.whatsapp_service.create_session(business_id)
        return result.json()
    
    async def get_session_status(self, business_id: str):
        result = await self.whatsapp_service.get_session_status(business_id)
        return result
    
    async def get_all_session(self):
        result = await self.whatsapp_service.get_all_sessions()
        return result
    
    async def delete_session(self, business_id: str):
        result = await self.whatsapp_service.delete_session(business_id)
        return result
    
    async def reconnect_session(self, business_id: str):
        result = await self.whatsapp_service.reconnect_session(business_id)
        return result
    
    async def send_message_controller(self, payload: SendMessagePayload):
        result = await self.whatsapp_service.send_message(payload)
        return result

    async def save_channel_data(self, business_id: str, payload: SaveChannelDataPayload):
        result = await self.whatsapp_service.save_channel_data(business_id, payload)
        return result.data