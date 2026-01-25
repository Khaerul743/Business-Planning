from dataclasses import dataclass
from typing import Any

from src.app.validators.message_schema import InsertNewMessage
from src.app.validators.whatsapp_schema import WebhookPayload
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IConversationRepository,
    IMessageRepository,
)
from src.infrastructure.meta import WhatsappManager


@dataclass
class SendTextMessageInput:
    business_id: int | None
    agent_id: int
    customer_id: int
    to_number: str
    text_message: str
    agent_response: str
    raw_webhook: WebhookPayload


@dataclass
class SendTextMessageOutput:
    conversation_id: int
    customer_message_id: int
    agent_message_id: int
    response_webhook: dict[str, Any]


class SendTextMessage(BaseUseCase[SendTextMessageInput, SendTextMessageOutput]):
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        message_repo: IMessageRepository,
        whatsapp_manager: WhatsappManager,
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.whatsapp_manager = whatsapp_manager

    async def execute(
        self, input_data: SendTextMessageInput
    ) -> UseCaseResult[SendTextMessageOutput]:
        try:
            raw_webhook = input_data.raw_webhook.model_dump()

            # get or insert conversation
            conversation = await self.conversation_repo.get_or_create_conversation(
                input_data.business_id, input_data.agent_id, input_data.customer_id
            )

            # Insert customer message
            customer_message = await self.message_repo.insert_new_message(
                conversation.id,
                InsertNewMessage(
                    sender_type="customer",
                    message_type="text",
                    content=input_data.text_message,
                    raw_webhook=raw_webhook,
                ),
            )

            # Insert agent message
            agent_message = await self.message_repo.insert_new_message(
                conversation.id,
                InsertNewMessage(
                    sender_type="ai",
                    message_type="text",
                    content=input_data.agent_response,
                    raw_webhook=raw_webhook,
                ),
            )

            result = self.whatsapp_manager.send_text_message(
                input_data.to_number, input_data.agent_response
            )

            return UseCaseResult.success_result(
                SendTextMessageOutput(
                    conversation_id=conversation.id,
                    customer_message_id=customer_message.id,
                    agent_message_id=agent_message.id,
                    response_webhook=result,
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error in send text message usecase: {str(e)}", e
            )
