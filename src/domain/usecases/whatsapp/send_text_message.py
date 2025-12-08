from dataclasses import dataclass

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.infrastructure.meta import WhatsappManager


@dataclass
class SendTextMessageInput:
    to_number: str
    text: str


@dataclass
class SendTextMessageOutput:
    to_number: str
    text: str
    status: str


class SendTextMessage(BaseUseCase[SendTextMessageInput, SendTextMessageOutput]):
    def __init__(self, whatsapp_manager: WhatsappManager):
        self.whatsapp_manager = whatsapp_manager

    def execute(
        self, input_data: SendTextMessageInput
    ) -> UseCaseResult[SendTextMessageOutput]:
        try:
            self.whatsapp_manager.send_text_message(
                input_data.to_number, input_data.text
            )
            return UseCaseResult.success_result(
                SendTextMessageOutput(input_data.to_number, input_data.text, "success")
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while sending text message: {e}", e
            )
