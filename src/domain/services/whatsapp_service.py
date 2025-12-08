from src.app.validators.whatsapp_schema import WebhookPayload
from src.domain.usecases.whatsapp import SendTextMessage, SendTextMessageInput
from src.infrastructure.meta import WhatsappManager

from .base import BaseService


class WhatsappService(BaseService):
    def __init__(self):
        super().__init__(__name__)

        # dependencies
        self.whatsapp_manager = WhatsappManager()

        # usecase
        self.send_text_message_usecase = SendTextMessage(self.whatsapp_manager)

    def _get_detail_message(self, webhook_payload: WebhookPayload):
        # Initialize defaults so they are always defined
        from_number = None
        message_type = None
        incoming_text = None

        for entry in webhook_payload.entry:
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})

                    # Cek apakah ada pesan (bukan status pesan)
                    if messages := value.get("messages"):
                        message_data = messages[0]
                        # Ambil data penting
                        from_number = message_data.get("from")  # Nomor pelanggan
                        message_type = message_data.get("type")
                        # Contoh: Balas pesan teks sederhana yang masuk
                        if message_type == "text":
                            incoming_text = message_data.get("text", {}).get(
                                "body", "Tidak ada teks"
                            )
                            print(f"Isi Pesan: {incoming_text}")
                        # Return after the first message is parsed
                        return from_number, message_type, incoming_text

        return from_number, message_type, incoming_text

    def send_text_message(self, payload: WebhookPayload):
        from_number, message_type, text = self._get_detail_message(payload)
        if from_number is None and text is None:
            return
        result = self.send_text_message_usecase.execute(
            SendTextMessageInput(from_number, text)
        )
        if not result.is_success():
            self.raise_error_usecase(result)
        return
