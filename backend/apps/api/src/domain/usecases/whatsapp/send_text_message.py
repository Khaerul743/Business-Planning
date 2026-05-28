from dataclasses import dataclass
from typing import Any, Literal
from uuid import UUID

from src.app.validators.message_schema import InsertNewMessage
from src.app.validators.whatsapp_schema import WebhookPayload
from src.core.exceptions.whatsapp_exceptions import ConversationNotFound
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IConversationRepository,
    ICustomerRepository,
    IMessageRepository,
)
from src.infrastructure.meta import WhatsappManager


@dataclass
class SendTextMessageInput:
    conversation_id: UUID
    sender_type: Literal["ai", "human_admin", "customer"]
    text_message: str


@dataclass
class SendTextMessageOutput:
    conversation_id: UUID
    response_webhook: dict[str, Any]


class SendTextMessage(BaseUseCase[SendTextMessageInput, SendTextMessageOutput]):
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        message_repo: IMessageRepository,
        customer_repo: ICustomerRepository,
        whatsapp_manager: WhatsappManager,
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.customer_repo = customer_repo
        self.whatsapp_manager = whatsapp_manager

    async def execute(
        self, input_data: SendTextMessageInput
    ) -> UseCaseResult[SendTextMessageOutput]:
        try:
            raw_webhook = {"type": "Direct response"}

            # Insert message
            agent_message = await self.message_repo.insert_new_message(
                input_data.conversation_id,
                InsertNewMessage(
                    sender_type=input_data.sender_type,
                    message_type="text",
                    content=input_data.text_message,
                    raw_webhook=raw_webhook,
                ),
            )

            # Get customer phone number
            phone_number = await self.customer_repo.get_phone_number_by_conversation_id(
                input_data.conversation_id
            )
            if phone_number is None:
                return UseCaseResult.error_result(
                    "Conversation not found", ConversationNotFound()
                )

            result = self.whatsapp_manager.send_text_message(
                phone_number, input_data.text_message
            )

            return UseCaseResult.success_result(
                SendTextMessageOutput(
                    conversation_id=input_data.conversation_id,
                    response_webhook=result,
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error in send text message usecase: {str(e)}", e
            )
