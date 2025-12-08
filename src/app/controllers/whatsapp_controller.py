from src.app.validators.whatsapp_schema import WebhookPayload
from src.domain.services import WhatsappService

from .base import BaseController


class WhatsappController(BaseController):
    def __init__(self):
        super().__init__(__name__)
        self.whatsapp_service = WhatsappService()

    def send_message(self, payload: WebhookPayload):
        try:
            if payload.object != "whatsapp_business_account":
                return
            self.whatsapp_service.send_text_message(payload)
            return

        except Exception as e:
            self._logger.error(f"Unexpected error while send message: {str(e)}")
            raise e
