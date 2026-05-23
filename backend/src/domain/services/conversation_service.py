from uuid import UUID

from supabase import AsyncClient

from src.core.context.request_context import current_user_id, current_user_email
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.core.exceptions.whatsapp_exceptions import (
    ConversationNotFound,
    CustomerNotFound,
)
from src.domain.repositories import (
    BusinessRepository,
    ConversationRepository,
    CustomerRepository,
    HumanFallbackRepository,
    MessageRepository,
)
from src.domain.usecases.conversation import (
    DeleteConversationFallbackInput,
    DeleteConversationUseCase,
    GetAllConversationInput,
    GetAllConversationUseCase,
)
from src.domain.usecases.whatsapp import SendTextMessage, SendTextMessageInput
from src.infrastructure.meta import WhatsappManager

from .base import BaseService


class ConversationService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        # Repositories
        self.conversation_repo = ConversationRepository(db)
        self.business_repo = BusinessRepository(db)
        self.message_repo = MessageRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.human_fallback_repo = HumanFallbackRepository(db)

        # dependencies
        self.whatsapp_manager = WhatsappManager()

        # Use case
        self.send_text_message_use_case = SendTextMessage(
            self.conversation_repo,
            self.message_repo,
            self.customer_repo,
            self.whatsapp_manager,
        )
        self.delete_conversation_fallback_usecase = DeleteConversationUseCase(
            self.conversation_repo, self.customer_repo, self.human_fallback_repo
        )
        self.get_all_conversation_usecase = GetAllConversationUseCase(
            self.conversation_repo, self.business_repo
        )

    async def _get_business_id(self, user_id: UUID) -> UUID | None:
        business_id = await self.business_repo.get_business_id_by_user_id(user_id)
        return business_id

    async def get_all_conversation(self, page: int = 1, limit: int = 10):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        if user_id is None:
            raise UnauthorizedException()

        self.logger.info(f"User {user_email}: Get all conversation")
        usc_result = await self.get_all_conversation_usecase.execute(
            GetAllConversationInput(user_id=user_id, page=page, limit=limit)
        )
        if not usc_result.is_success():
            self.logger.warning(f"User {user_email}: Failed to get all conversation")
            self.raise_error_usecase(usc_result)

        result_data = usc_result.get_data()
        if result_data is None:
            self.logger.warning(f"User {user_email}: get all conversation usecase did not return the data")
            raise RuntimeError("get all conversation usecase did not return the data")

        list_data = []
        for i in result_data.conversations:
            del i["agent_id"]
            del i["business_id"]
            list_data.append(i)

        self.logger.info(f"User {user_email}: Get all conversation is successfully")
        return {
            "conversations": list_data,
            "total": result_data.total,
            "page": result_data.page,
            "limit": result_data.limit,
        }

    async def get_all_messages(self, conversation_id: UUID):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Get all messages")
        messages = await self.message_repo.get_all_message_by_conversation_id(
            conversation_id
        )

        self.logger.info(f"User {user_email}: Get all messages is successfully")
        return messages

    async def get_conversation_fallback(self, conversation_id: UUID):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Get conversation fallback")
        conversation_fallback = await self.human_fallback_repo.get_human_fallback_by_id(
            conversation_id
        )
        if conversation_fallback is None:
            self.logger.warning(f"User {user_email}: Conversation not found")
            raise ConversationNotFound()
        self.logger.info(f"User {user_email}: Get conversation fallback is successfully")
        return conversation_fallback

    async def get_all_conversation_with_human_fallback(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        if user_id is None:
            raise UnauthorizedException()
        business_id = await self._get_business_id(user_id)
        if business_id is None:
            self.logger.warning(f"User {user_email}: Business not found")
            raise BusinessNotFound()

        self.logger.info(f"User {user_email}: Get all conversation with human fallback")
        conversation_human_fallbacks = (
            await self.human_fallback_repo.get_all_human_fallback_by_business_id(
                business_id
            )
        )

        if conversation_human_fallbacks is None:
            self.logger.info(f"User {user_email}: Get all conversation with human fallback is successfully")
            return []

        self.logger.info(f"User {user_email}: Get all conversation with human fallback is successfully")
        return conversation_human_fallbacks

    async def post_new_message(self, conversation_id: UUID, text_message: str):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Post new message")
        conversation = await self.conversation_repo.get_conversation_by_id(
            conversation_id
        )
        if conversation is None:
            self.logger.warning(f"User {user_email}: Conversation not found")
            raise ConversationNotFound()

        send_message_result = await self.send_text_message_use_case.execute(
            SendTextMessageInput(conversation.id, "human_admin", text_message)
        )

        if not send_message_result.is_success():
            self.logger.warning(f"User {user_email}: Failed to post new message")
            self.raise_error_usecase(send_message_result)

        result_data = send_message_result.get_data()
        if result_data is None:
            self.logger.warning(f"User {user_email}: Send message use case did not returned the data")
            raise RuntimeError("Send message use case did not returned the data")

        self.logger.info(f"User {user_email}: Post new message is successfully")
        return result_data

    async def get_customer_status_agent(self, conversation_id: UUID):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Get customer status agent")
        conversation = await self.conversation_repo.get_conversation_by_id(
            conversation_id
        )
        if conversation is None:
            self.logger.warning(f"User {user_email}: Conversation not found")
            raise ConversationNotFound()

        customer_id = conversation.customer_id
        if customer_id is None:
            self.logger.warning(f"User {user_email}: Customer not found: id {customer_id}")
            raise CustomerNotFound()

        customer_status_agent = (
            await self.customer_repo.get_customer_status_agent_by_customer_id(
                customer_id
            )
        )
        if customer_status_agent is None:
            self.logger.warning(f"User {user_email}: Customer status agent not found")
            raise CustomerNotFound()

        self.logger.info(f"User {user_email}: Get customer status agent is successfully")
        return customer_status_agent

    async def update_customer_status_agent(self, conversation_id: UUID, status: bool):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Update customer status agent")
        conversation = await self.conversation_repo.get_conversation_by_id(
            conversation_id
        )
        if conversation is None:
            self.logger.warning(f"User {user_email}: Conversation not found")
            raise ConversationNotFound()

        customer_id = conversation.customer_id
        if customer_id is None:
            self.logger.warning(f"User {user_email}: Customer not found: id {customer_id}")
            raise CustomerNotFound()

        updated_customer = await (
            self.customer_repo.update_customer_status_agent_by_customer_id(
                customer_id, status
            )
        )
        if updated_customer is None:
            self.logger.warning(f"User {user_email}: Customer not found")
            raise CustomerNotFound()

        self.logger.info(f"User {user_email}: Update customer status agent is successfully")
        return updated_customer

    async def delete_conversation_fallback(self, conversation_id: UUID):
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: Delete conversation fallback")
        usc_result = await self.delete_conversation_fallback_usecase.execute(
            DeleteConversationFallbackInput(conversation_id)
        )
        if not usc_result.is_success():
            self.logger.warning(f"User {user_email}: Failed to delete conversation fallback")
            self.raise_error_usecase(usc_result)

        result_data = usc_result.get_data()
        if result_data is None:
            self.logger.warning(f"User {user_email}: delete conversation fallback usecase did not return the data")
            raise RuntimeError(
                "delete conversation fallback usecase did not return the data"
            )

        self.logger.info(f"User {user_email}: Delete conversation fallback is successfully")
        return result_data.result
