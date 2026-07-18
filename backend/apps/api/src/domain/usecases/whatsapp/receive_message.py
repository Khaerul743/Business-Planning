from uuid import UUID
from dataclasses import dataclass
from src.domain.usecases.base import UseCaseResult, BaseUseCase
from src.app.validators.customer_schema import InsertNewCustomer
from src.app.validators.whatsapp_schema import WebhookPayload
from .message_processing import MessageProcessingUseCase, MessageProcessingUseCaseInput
from .save_conversation import SaveConversationInput, SaveConversationUseCase
from .send_text_message import SendTextMessage, SendTextMessageInput


@dataclass
class ReceiveMessageInput:
    agent_id: UUID
    business_id: UUID
    phone_number_id: str
    customer_data: InsertNewCustomer
    text_message: str
    raw_webhook: WebhookPayload


@dataclass
class ReceiveMessageOutput:
    success: bool = True


class ReceiveMessageUseCase(BaseUseCase[ReceiveMessageInput, ReceiveMessageOutput]):
    def __init__(
        self,
        message_processing: MessageProcessingUseCase,
        save_conversation: SaveConversationUseCase,
        send_text_message: SendTextMessage,
    ):
        self.message_processing = message_processing
        self.save_conversation = save_conversation
        self.send_text_message = send_text_message

        super().__init__(__name__)

    def raise_error_usecase(self, use_case: UseCaseResult, error_message: str):
        exception = use_case.get_exception()
        if exception:
            print(exception)
            return UseCaseResult.error_result(error_message, exception)
        return UseCaseResult.error_result("Unexpected usecase error")

    async def execute(
        self, input_data: ReceiveMessageInput
    ) -> UseCaseResult[ReceiveMessageOutput]:
        try:
            self.logger.info("Executing message processing usecase")
            result_message = await self.message_processing.execute(
                MessageProcessingUseCaseInput(
                    input_data.agent_id,
                    input_data.business_id,
                    input_data.phone_number_id,
                    input_data.customer_data,
                    text_message=input_data.text_message
                )
            )
            if not result_message.is_success():
                return self.raise_error_usecase(
                    result_message, "message processing usecase isn't successfully"
                )

            result_message_data = result_message.get_data()
            if result_message_data is None:
                return UseCaseResult.error_result(
                    "Message processing usecase did not return the data",
                    RuntimeError("Message processing usecase didnot return the data"),
                )
            self.logger.info("Executing message processing usecase is successfully")
            self.logger.info("Executing save conversation usecase")
            # Save conversation
            result_sv_conv = await self.save_conversation.execute(
                SaveConversationInput(
                    input_data.business_id,
                    input_data.agent_id,
                    result_message_data.customer_id,
                    result_message_data.text_message,
                    input_data.raw_webhook,
                    result_message_data.detail_agent_output,
                )
            )
            if not result_sv_conv.is_success():
                return self.raise_error_usecase(
                    result_sv_conv, "Save conversation usecase isn't successfully"
                )

            result_sv_conv_data = result_sv_conv.get_data()
            if result_sv_conv is None:
                return UseCaseResult.error_result(
                    "Save conversation usecase did not return the data",
                    RuntimeError("Save conversation usecase did not return the data"),
                )

            self.logger.info("Executing save conversation usecase is successfully")
            self.logger.info("Executing send message usecase")
            # Send text message
            result_send_text = await self.send_text_message.execute(
                SendTextMessageInput(
                    result_sv_conv_data.conversation_id,
                    "ai",
                    result_message_data.response,
                    business_id=str(input_data.business_id)
                )
            )

            if not result_send_text.is_success():
                return self.raise_error_usecase(
                    result_send_text, "Send text message usecase isnt successfully"
                )

            result_send_text_data = result_send_text.get_data()
            if result_send_text_data is None:
                return UseCaseResult.error_result(
                    "send text message did not returned the data"
                )
            self.logger.info("Executing send message usecase is successfully")
            return UseCaseResult.success_result(ReceiveMessageOutput())
        except Exception as e:
            return UseCaseResult.error_result(
                "Unexpected error in Receive message usecase", e
            )
