from supabase import AsyncClient

from src.app.validators.customer_schema import InsertNewCustomer
from src.app.validators.whatsapp_schema import FilteredPayload, WebhookPayload
from src.domain.repositories import (
    AgentConfigurationRepository,
    AgentRepository,
    BusinessRepository,
    ConversationRepository,
    CustomerRepository,
    MessageRepository,
)
from src.domain.usecases.whatsapp import (
    MessageProcessingUseCase,
    MessageProcessingUseCaseInput,
    SendTextMessage,
    SendTextMessageInput,
)
from src.infrastructure.ai.agent.manager import whatsapp_agent_manager
from src.infrastructure.ai.agent.whatsapp_agent import WhatsappAgentState
from src.infrastructure.meta import WhatsappManager

from .base import BaseService


class WhatsappService(BaseService):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)

        # repositories
        self.business_repo = BusinessRepository(db)
        self.agent_repo = AgentRepository(db)
        self.customer_repo = CustomerRepository(db)
        self.agent_conf_repo = AgentConfigurationRepository(db)
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)

        # dependencies
        self.whatsapp_manager = WhatsappManager()
        self.whatsapp_agent_manager = whatsapp_agent_manager

        # usecase
        self.message_processing_usecase = MessageProcessingUseCase(
            self.customer_repo, self.agent_conf_repo, self.whatsapp_agent_manager
        )
        self.send_text_message_usecase = SendTextMessage(
            self.conversation_repo, self.message_repo, self.whatsapp_manager
        )

    def _get_detail_message(
        self, webhook_payload: WebhookPayload
    ) -> FilteredPayload | None:
        for entry in webhook_payload.entry:
            for change in entry.get("changes", []):
                if change.get("field") == "messages":
                    value = change.get("value", {})

                    # Ekstrak phone_number_id (ID nomor bisnis Anda)
                    phone_number_id = value.get("metadata", {}).get("phone_number_id")

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
                            phone_number_id=str(phone_number_id)
                            if phone_number_id
                            else "unknown",
                            wa_id=wa_id,
                            name=name,
                            from_number=from_number,
                            message_type=message_type,
                            text=incoming_text,
                        )

        return None

    async def send_text_message(self, payload: WebhookPayload):
        try:
            filtered_payload = self._get_detail_message(payload)

            if filtered_payload is None:
                raise RuntimeWarning("Filtered payload is None")

            agent = await self.agent_repo.get_agent_by_phone_number_id(
                filtered_payload.phone_number_id
            )

            if agent is None:
                raise RuntimeWarning("Agent not found")

            if not agent.enable_ai:
                raise RuntimeWarning("agent is not active")

            customer_data = InsertNewCustomer(
                wa_id=filtered_payload.wa_id,
                name=filtered_payload.name,
                phone_number=filtered_payload.from_number,
            )

            agent_state = WhatsappAgentState(
                messages=[], user_message=filtered_payload.text
            )
            message_processing_result = await self.message_processing_usecase.execute(
                MessageProcessingUseCaseInput(
                    agent.id, agent.phone_number_id, customer_data, agent_state
                )
            )

            if not message_processing_result.is_success():
                self.raise_error_usecase(message_processing_result)

            message_processing_result_data = message_processing_result.get_data()
            if message_processing_result_data is None:
                raise RuntimeError("Message processing usecase did not returned data")

            send_text_message_result = await self.send_text_message_usecase.execute(
                SendTextMessageInput(
                    agent.business_id,
                    agent.id,
                    customer_id=message_processing_result_data.customer_id,
                    to_number=filtered_payload.from_number,
                    text_message=message_processing_result_data.text_message,
                    agent_response=message_processing_result_data.response,
                    raw_webhook=payload,
                )
            )

            if not send_text_message_result.is_success():
                self.raise_error_usecase(send_text_message_result)

            print(send_text_message_result.get_data())

        except RuntimeWarning as e:
            self.logger.warning(str(e))

        except Exception as e:
            self.logger.error(str(e))

        finally:
            return {"status": "receive"}
