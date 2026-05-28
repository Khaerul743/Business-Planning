from dataclasses import dataclass
from uuid import UUID

from src.core.exceptions.whatsapp_exceptions import ConversationNotFound
from src.domain.models import Human_Fallback
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IConversationRepository,
    ICustomerRepository,
    IHumanFallbackRepository,
)


@dataclass
class DeleteConversationFallbackInput:
    conversation_id: UUID


@dataclass
class DeleteConversationFallbackOutput:
    result: Human_Fallback


class DeleteConversationUseCase(
    BaseUseCase[DeleteConversationFallbackInput, DeleteConversationFallbackOutput]
):
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        customer_repo: ICustomerRepository,
        human_fallback_repo: IHumanFallbackRepository,
    ):
        self.conversation_repo = conversation_repo
        self.customer_repo = customer_repo
        self.human_fallback_repo = human_fallback_repo

    async def execute(
        self, input_data: DeleteConversationFallbackInput
    ) -> UseCaseResult[DeleteConversationFallbackOutput]:
        try:
            # Get conversation
            conversation = await self.conversation_repo.get_conversation_by_id(
                input_data.conversation_id
            )
            if conversation is None:
                return UseCaseResult.error_result(
                    "Conversation not found", ConversationNotFound()
                )

            # Delete conversation fallback
            result = (
                await self.human_fallback_repo.delete_human_fallback_by_conversation_id(
                    conversation.id
                )
            )
            if result is None:
                return UseCaseResult.error_result(
                    "Conversation fallback not found", ConversationNotFound()
                )

            # Set Conversation status to false
            await self.conversation_repo.update_conversation_status(
                conversation.id, False
            )

            # Update customer status agent
            await self.customer_repo.update_customer_status_agent_by_customer_id(
                conversation.customer_id, True
            )

            return UseCaseResult.success_result(
                DeleteConversationFallbackOutput(result=result)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while deleting conversation fallback: {e}", e
            )
