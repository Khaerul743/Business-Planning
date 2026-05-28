from uuid import uuid4
from supabase import AsyncClient

from src.app.validators.whatsapp_schema import FilteredPayload, WebhookPayload
from src.domain.repositories import (
    AgentRepository,
)
from src.infrastructure.queue.redis import redis_client
from src.infrastructure.queue import RedisQueue


from .base import BaseService


class WhatsappService(BaseService):
    def __init__(self, db: AsyncClient):
        super().__init__(__name__)

        # queue
        self.redis_queue = RedisQueue(redis_client, "message_queue")

        # repositories
        # self.business_repo = BusinessRepository(db)
        self.agent_repo = AgentRepository(db)
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
            # payload_queue = {
            #     "queue_id": "121233",
            #     "type": "invoke_agent",
            #     "retry": 0,
            #     "job_payload": {
            #         "user_message": "hello",
            #         "phone_number_id": "12345678",
            #         "agent_id": "a04b8eb2-3b32-44e2-9a6a-bbca2c23ab58",
            #         "business_id": "06a8a34c-12f8-42c6-bf09-33f2e3a08171",
            #         "webhook_payload": {"object": "str", "entry": ["test", "entry"]},
            #         "customer_data": {
            #             "wa_id": "02899239",
            #             "phone_number": "0493940054",
            #             "name": "rusdi",
            #         },
            #     },
            # }
            self.redis_queue.enqueue(payload_queue)
            print("REDIS QUEUE PUSH")
            # if agent is None:
            #     raise RuntimeWarning("Agent not found")

            # if not agent.enable_ai:
            #     raise RuntimeWarning("agent is not active")

            # customer_data = InsertNewCustomer(
            #     wa_id=filtered_payload.wa_id,
            #     name=filtered_payload.name,
            #     phone_number=filtered_payload.from_number,
            # )

            # agent_state = WhatsappAgentState(
            #     messages=[], user_message=filtered_payload.text
            # )
            # message_processing_result = await self.message_processing_usecase.execute(
            #     MessageProcessingUseCaseInput(
            #         agent.id,
            #         agent.business_id,
            #         agent.phone_number_id,
            #         customer_data,
            #         agent_state,
            #     )
            # )

            # if not message_processing_result.is_success():
            #     self.raise_error_usecase(message_processing_result)

            # message_processing_result_data = message_processing_result.get_data()
            # if message_processing_result_data is None:
            #     raise RuntimeError("Message processing usecase did not returned data")

            # print(f"Message processing result: \n{message_processing_result_data}")
            # save_conversation_result = await self.save_conversation_usecase.execute(
            #     SaveConversationInput(
            #         agent.business_id,
            #         agent.id,
            #         message_processing_result_data.customer_id,
            #         message_processing_result_data.text_message,
            #         payload,
            #         message_processing_result_data.detail_agent_output,
            #     )
            # )

            # if not save_conversation_result.is_success():
            #     self.raise_error_usecase(save_conversation_result)

            # save_conversation_data = save_conversation_result.get_data()

            # if save_conversation_data is None:
            #     raise RuntimeError("Save conversation usecase did not returned data")

            # send_text_message_result = await self.send_text_message_usecase.execute(
            #     SendTextMessageInput(
            #         conversation_id=save_conversation_data.conversation_id,
            #         text_message=message_processing_result_data.response,
            #         sender_type="ai",
            #     )
            # )

            # if not send_text_message_result.is_success():
            #     self.raise_error_usecase(send_text_message_result)

        except RuntimeWarning as e:
            self.logger.warning(str(e))

        except Exception as e:
            self.logger.error(str(e))
            raise e

        finally:
            return {"status": "receive"}
