from dataclasses import dataclass
from uuid import UUID

from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IBusinessRepository,
    IConversationRepository,
)


@dataclass
class GetAllConversationInput:
    user_id: UUID
    page: int
    limit: int


@dataclass
class GetAllConversationOutput:
    conversations: list[dict]
    total: int
    page: int
    limit: int


class GetAllConversationUseCase(
    BaseUseCase[GetAllConversationInput, GetAllConversationOutput]
):
    def __init__(
        self,
        conversation_repo: IConversationRepository,
        business_repo: IBusinessRepository,
    ):
        self.conversation_repo = conversation_repo
        self.business_repo = business_repo

    async def execute(
        self, input_data: GetAllConversationInput
    ) -> UseCaseResult[GetAllConversationOutput]:
        try:
            # Validate user authentication
            if input_data.user_id is None:
                return UseCaseResult.error_result(
                    "Unauthorized", UnauthorizedException()
                )

            # Get business_id from user_id
            business_id, _ = (
                await self.business_repo.get_business_id_n_agent_id_by_user_id(
                    input_data.user_id
                )
            )
            if business_id is None:
                return UseCaseResult.error_result(
                    "Business not found", BusinessNotFound()
                )

            # Calculate offset from page and limit
            offset = (input_data.page - 1) * input_data.limit

            # Fetch paginated conversations with last message
            conversations, total = (
                await self.conversation_repo.get_paginated_conversations_by_business_id(
                    business_id, input_data.limit, offset
                )
            )

            return UseCaseResult.success_result(
                GetAllConversationOutput(
                    conversations=conversations,
                    total=total,
                    page=input_data.page,
                    limit=input_data.limit,
                )
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while fetching conversations: {e}", e
            )
