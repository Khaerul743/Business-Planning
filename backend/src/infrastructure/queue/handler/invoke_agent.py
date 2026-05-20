from supabase import AsyncClient
from src.domain.usecases.whatsapp import (
    MessageProcessingUseCase,
    SaveConversationUseCase,
    HumanFallbackUseCase,
    SendTextMessage,
    ReceiveMessageUseCase,
    ReceiveMessageInput,
)
from src.domain.repositories import (
    CustomerRepository,
    AgentConfigurationRepository,
    AnalyticsRepository,
    BusinessRepository,
    DocumentKnowladgeRepository,
    BusinessKnowladgeRepository,
    HumanFallbackRepository,
    ConversationRepository,
    MessageRepository,
)
from src.app.validators.customer_schema import InsertNewCustomer
from src.app.validators.whatsapp_schema import WebhookPayload
from src.infrastructure.meta import WhatsappManager
from src.domain.usecases.agent import CreateAgentObjUseCase
from src.infrastructure.ai.agent.wa_agent import WhatsappAgentState

from src.infrastructure.ai.agent.manager import whatsapp_agent_manager
from .base import BaseJobHandler, BaseJob


class InvokeAgentHandler(BaseJobHandler):
    def __init__(self, db: AsyncClient):
        self.db = db
        # Repositories
        self.customer_repo = CustomerRepository(self.db)
        self.agent_conf_repo = AgentConfigurationRepository(self.db)
        self.analytic_repo = AnalyticsRepository(self.db)
        self.business_repo = BusinessRepository(self.db)
        self.document_knowladge_repo = DocumentKnowladgeRepository(self.db)
        self.business_knowladge_repo = BusinessKnowladgeRepository(self.db)
        self.conversation_repo = ConversationRepository(self.db)
        self.message_repo = MessageRepository(self.db)
        self.human_fallback_repo = HumanFallbackRepository(self.db)

        # util
        self.whatsapp_manager = WhatsappManager()

        # usecases
        self.create_agent_obj_usecase = CreateAgentObjUseCase(
            self.agent_conf_repo,
            self.business_repo,
            self.document_knowladge_repo,
            self.business_knowladge_repo,
            whatsapp_agent_manager,
        )
        self.message_processing_usecase = MessageProcessingUseCase(
            self.customer_repo,
            self.agent_conf_repo,
            self.analytic_repo,
            whatsapp_agent_manager,
            self.create_agent_obj_usecase,
        )
        self.human_fallback_usecase = HumanFallbackUseCase(
            self.human_fallback_repo, self.conversation_repo
        )
        self.save_conversation_usecase = SaveConversationUseCase(
            self.conversation_repo, self.message_repo, self.human_fallback_usecase
        )
        self.send_text_message_usecase = SendTextMessage(
            self.conversation_repo,
            self.message_repo,
            self.customer_repo,
            self.whatsapp_manager,
        )
        self.receive_message_usecase = ReceiveMessageUseCase(
            self.message_processing_usecase,
            self.save_conversation_usecase,
            self.send_text_message_usecase,
        )

    async def handle(self, job: BaseJob):
        payload = job.job_payload
        customer_data = InsertNewCustomer(
            wa_id=payload["customer_data"]["wa_id"],
            phone_number=payload["customer_data"]["phone_number"],
            name=payload["customer_data"]["name"],
        )
        agent_state = WhatsappAgentState(
            messages=[], user_message=payload["user_message"]
        )
        webhook_payload = WebhookPayload.model_validate(payload["webhook_payload"])
        input_data = ReceiveMessageInput(
            payload["agent_id"],
            payload["business_id"],
            payload["phone_number_id"],
            customer_data,
            agent_state,
            webhook_payload,
        )
        await self.receive_message_usecase.execute(input_data)
        return None
