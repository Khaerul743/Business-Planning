from uuid import uuid4, UUID
from supabase import AsyncClient

from src.app.validators.whatsapp_schema import FilteredPayload, WebhookPayload
from src.domain.repositories import (
    AgentRepository,
)
from src.infrastructure.queue.redis import redis_client
from src.infrastructure.queue import RedisQueue
from src.infrastructure.whatsapp_session import whatsapp_session_manager
from src.domain.repositories import BusinessRepository, WhatsappChannelRepository
from src.core.exceptions.business_exception import BusinessNotFound
from src.app.validators.whatsapp_schema import SendMessagePayload
from src.app.validators.wa_service_schema import SaveChannelDataPayload
from src.domain.usecases.whatsapp.save_channel_data import SaveChannelDataUseCase, SaveChannelDataInput
from .base import BaseService


class WhatsappService(BaseService):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)

        # queue
        self.redis_queue = RedisQueue(redis_client, "message_queue")

        # repositories
        self.business_repo = BusinessRepository(db)
        self.agent_repo = AgentRepository(db)
        self.channel_repo = WhatsappChannelRepository(db)
        # self.customer_repo = CustomerRepository(db)
        # self.agent_conf_repo = AgentConfigurationRepository(db)
        # self.conversation_repo = ConversationRepository(db)
        # self.message_repo = MessageRepository(db)
        # self.analytic_repo = AnalyticsRepository(db)
        # self.human_fallback_repo = HumanFallbackRepository(db)
        # self.document_knowladge_repo = DocumentKnowladgeRepository(db)
        # self.business_knowladge_repo = BusinessKnowladgeRepository(db)
        # # dependencies
        # self.whatsapp_manager = WhatsappManager()
        # self.whatsapp_agent_manager = whatsapp_agent_manager

        # # usecase
        # self.create_agent_obj_usecase = CreateAgentObjUseCase(
        #     self.agent_conf_repo,
        #     self.business_repo,
        #     self.document_knowladge_repo,
        #     self.business_knowladge_repo,
        #     self.whatsapp_agent_manager,
        # )
        # self.message_processing_usecase = MessageProcessingUseCase(
        #     self.customer_repo,
        #     self.agent_conf_repo,
        #     self.analytic_repo,
        #     self.whatsapp_agent_manager,
        #     self.create_agent_obj_usecase,
        # )
        # self.send_text_message_usecase = SendTextMessage(
        #     self.conversation_repo,
        #     self.message_repo,
        #     self.customer_repo,
        #     self.whatsapp_manager,
        # )
        # self.human_fallback_usecase = HumanFallbackUseCase(self.human_fallback_repo)
        # self.save_conversation_usecase = SaveConversationUseCase(
        #     self.conversation_repo, self.message_repo, self.human_fallback_usecase
        # )

    def _get_detail_message(
        self, webhook_payload: WebhookPayload
    ) -> FilteredPayload | None:
        for entry in webhook_payload.entry:
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})

                    # Ekstrak phone_number_id (ID nomor bisnis Anda)
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")
                    is_from_wa_service = value.get("metadata", {}).get("is_from_wa_service", False)

                    # Inisialisasi variabel pendukung
                    name = None
                    wa_id = None
                    from_number = None
                    message_type = None
                    incoming_text = None

                    # 1. Ekstrak data profil (Nama & WA ID) dari array contacts
                    if contacts := value.get("contacts"):
                        contact_data = contacts[0]
                        name = contact_data.get("profile", {}).get("name")
                        wa_id = contact_data.get("wa_id")

                    # 2. Ekstrak data pesan dari array messages
                    if messages := value.get("messages"):
                        message_data = messages[0]
                        from_number = message_data.get("from")
                        message_type = message_data.get("type")

                        if message_type == "text":
                            incoming_text = message_data.get("text", {}).get("body")
                        elif message_type == "interactive":
                            # Handling button reply atau list reply
                            interactive = message_data.get("interactive", {})
                            if interactive.get("type") == "button_reply":
                                incoming_text = interactive.get("button_reply", {}).get(
                                    "title"
                                )
                            elif interactive.get("type") == "list_reply":
                                incoming_text = interactive.get("list_reply", {}).get(
                                    "title"
                                )

                        # Mengembalikan objek FilteredPayload
                        return FilteredPayload(
                            phone_number_id=(
                                str(phone_number_id) if phone_number_id else "unknown"
                            ),
                            wa_id=wa_id,
                            name=name,
                            from_number=from_number,
                            message_type=message_type,
                            text=incoming_text,
                            is_from_wa_service=is_from_wa_service,
                        )

        return None

    async def send_text_message(self, payload: WebhookPayload):
        try:
            filtered_payload = self._get_detail_message(payload)

            if filtered_payload is None:
                raise RuntimeWarning("Filtered payload is None")

            if filtered_payload.is_from_wa_service:
                agent = await self.agent_repo.get_agent_by_business_id(UUID(filtered_payload.phone_number_id))
                print(f"Agent: {agent}")
            else:
                agent = await self.agent_repo.get_agent_by_phone_number_id(
                    filtered_payload.phone_number_id
                )
                
            if agent is None:
                return

            queue_id = uuid4()
            payload_queue = {
                "queue_id": str(queue_id),
                "type": "invoke_agent",
                "retry": 0,
                "job_payload": {
                    "user_message": filtered_payload.text,
                    "phone_number_id": agent.phone_number_id,
                    "agent_id": str(agent.id),
                    "business_id": str(agent.business_id),
                    "webhook_payload": payload.model_dump(),
                    "customer_data": {
                        "wa_id": filtered_payload.wa_id,
                        "phone_number": filtered_payload.from_number,
                        "name": filtered_payload.name,
                    },
                },
            }
            print(payload_queue)
            self.redis_queue.enqueue(payload_queue)
            print("REDIS QUEUE PUSH")

        except RuntimeWarning as e:
            self.logger.warning(str(e))

        except Exception as e:
            self.logger.error(str(e))
            raise e

        finally:
            return {"status": "receive"}
    
    
    async def create_session(self, business_id: str):
        business = await self.business_repo.get_business_by_id(UUID(business_id))
        if business is None:
            raise BusinessNotFound()
        
        result = whatsapp_session_manager.create_session(business_id)
        return result.data
    
    async def get_session_status(self, business_id: str):
        business = await self.business_repo.get_business_by_id(UUID(business_id))
        if business is None:
            raise BusinessNotFound()
        
        result = whatsapp_session_manager.get_session_status(business_id)
        return result.data
    
    async def get_all_sessions(self):
        result = whatsapp_session_manager.get_all_session()
        return result.data
    
    async def delete_session(self, business_id: str):
        business = await self.business_repo.get_business_by_id(UUID(business_id))
        if business is None:
            raise BusinessNotFound()
        
        result = whatsapp_session_manager.delete_session(business_id)
        return result.data     
    
    async def reconnect_session(self, business_id: str):
        business = await self.business_repo.get_business_by_id(UUID(business_id))
        if business is None:
            raise BusinessNotFound()
        
        result = whatsapp_session_manager.reconnect_session(business_id)
        return result.data

    async def send_message(self, payload: SendMessagePayload):
        business = await self.business_repo.get_business_by_id(UUID(payload.business_id))
        if business is None:
            raise BusinessNotFound()
        
        result = whatsapp_session_manager.send_message(payload)
        return result.data

    async def save_channel_data(self, business_id: str, payload: SaveChannelDataPayload):
        usecase = SaveChannelDataUseCase(self.channel_repo)
        input_data = SaveChannelDataInput(
            business_id=UUID(business_id),
            phone_number=payload.phone_number,
            status=payload.status,
            display_name=payload.display_name
        )
        result = await usecase.execute(input_data)
        if not result.is_success():
            self.raise_error_usecase(result)
        return result.get_data()
