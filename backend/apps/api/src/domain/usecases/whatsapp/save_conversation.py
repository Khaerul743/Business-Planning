from dataclasses import dataclass
from uuid import UUID

from src.app.validators.human_fallback_schema import InsertNewHumanFallback
from src.app.validators.message_schema import InsertNewMessage
from src.app.validators.whatsapp_schema import WebhookPayload
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IConversationRepository, IMessageRepository

from .human_fallback import HumanFallbackInput, HumanFallbackUseCase


@dataclass
class SaveConversationInput:
    business_id: UUID | None
    agent_id: UUID
    customer_id: UUID
    text_message: str
    raw_webhook: WebhookPayload
    detail_agent_output: dict


@dataclass
class SaveConversationOutput:
    conversation_id: UUID


class SaveConversationUseCase(
    BaseUseCase[SaveConversationInput, SaveConversationOutput]
):
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        message_repo: IMessageRepository,
        human_fallback_usecase: HumanFallbackUseCase,
    ):
        self.conversation_repo = conversation_repo
        self.message_repo = message_repo
        self.human_fallback_usecase = human_fallback_usecase

        super().__init__(__name__)

    async def execute(
        self, input_data: SaveConversationInput
    ) -> UseCaseResult[SaveConversationOutput]:
        try:
            raw_webhook = input_data.raw_webhook.model_dump()
            self.logger.info("Get or insert conversation data")
            # get or insert conversation
            conversation = await self.conversation_repo.get_or_create_conversation(
                input_data.business_id, input_data.agent_id, input_data.customer_id
            )

            self.logger.info("Insert customer message")
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

            if input_data.detail_agent_output["fallback_human"]:
                self.logger.info("Insert new human fallback")
                payload = InsertNewHumanFallback(
                    business_id=input_data.business_id,
                    conversation_id=conversation.id,
                    confidence_level=input_data.detail_agent_output["confidence_level"],
                    last_decision_summary=input_data.detail_agent_output[
                        "handoff_reason"
                    ],
                )
                await self.human_fallback_usecase.execute(
                    HumanFallbackInput(payload, input_data.customer_id)
                )

            return UseCaseResult.success_result(
                SaveConversationOutput(conversation_id=conversation.id)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while saving conversation: {e}", e
            )
