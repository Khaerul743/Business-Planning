from supabase import AsyncClient

from src.app.validators.whatsapp_schema import WebhookPayload
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
