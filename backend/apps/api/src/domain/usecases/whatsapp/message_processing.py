from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from time import perf_counter

from src.app.validators.analytic_schema import InsertAgentAnalytic
from src.app.validators.customer_schema import InsertNewCustomer
from src.domain.models.agent_analytics import AgentAnalytics
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAnalyticRepository,
    ICustomerRepository,
)
from src.infrastructure.langgraph_server import langgraph_client
from src.domain.usecases.agent_new import InvokeCSAgent, InvokeCSAgentInput

@dataclass
class MessageProcessingUseCaseInput:
    agent_id: UUID
    business_id: UUID
    phone_number_id: str
    customer_data: InsertNewCustomer
    text_message: str


@dataclass
class MessageProcessingUseCaseOutput:
    customer_id: UUID
    text_message: str
    response: str
    detail_agent_output: dict


class MessageProcessingUseCase(
    BaseUseCase[MessageProcessingUseCaseInput, MessageProcessingUseCaseOutput]
):
    def __init__(
        self,
        customer_repo: ICustomerRepository,
        analytic_repo: IAnalyticRepository,
        invoke_cs_agent_usecase: InvokeCSAgent
    ):
        self.customer_repo: ICustomerRepository = customer_repo
        self.analytic_repo = analytic_repo
        self.invoke_cs_agent_usecase = invoke_cs_agent_usecase

        super().__init__(__name__)

    async def execute(
        self, input_data: MessageProcessingUseCaseInput
    ) -> UseCaseResult[MessageProcessingUseCaseOutput]:
        try:
            self.logger.info("Insert or get customer data")
            # Insert new or get customer
            customer, is_new_customer = await self.customer_repo.get_or_insert_custormer(
                input_data.agent_id, input_data.customer_data
            )
            if not customer.enable_ai:
                return UseCaseResult.error_result(
                    f"The user is disable this customer: customer phone number {customer.phone_number}",
                    RuntimeWarning(
                        f"The user is disable this customer: customer phone number {customer.phone_number}"
                    ),
                )

            if is_new_customer:
                self.logger.info("Register new thread id")
                thread_id = await langgraph_client.register_thread_id(customer.id)
            else:
                self.logger.info("Thread id is registered")
                thread_id = customer.id

            self.logger.info("Executing invoke agent cs usecase")
            start_time = perf_counter()
            usecase_result = await self.invoke_cs_agent_usecase.execute(InvokeCSAgentInput(input_data.agent_id, str(thread_id), input_data.text_message))
            response_time = perf_counter() - start_time
            if not usecase_result.is_success():
                self.logger.error(f"invoke agent usecase is error")
                return UseCaseResult.error_result("invoke agent usecase is error", RuntimeError("invoke agent usecase is error"))

            agent_result = usecase_result.get_data()
            if agent_result is None:
                return UseCaseResult.error_result("Invoke agent usecase did not returned the data",RuntimeError("Invoke agent usecase did not returned the data")) 
            
            self.logger.info("Executing invoke agent cs usecase is successfully")
            # Insert Agent Analytic
            date_now = datetime.now().date()
            
            self.logger.info("Insert agent analytics data")
            agent_analytic: AgentAnalytics = (
                await self.analytic_repo.insert_agent_analytic(
                    input_data.agent_id,
                    InsertAgentAnalytic(
                        date=str(date_now),
                        total_message=2,
                        response_time=response_time,
                        token=agent_result["token_usage"],
                        ai_response=agent_result["response"],
                        human_takeover=agent_result["fallback_human"],
                        user_message=agent_result["user_message"],
                        category=agent_result["category"],
                        is_business_related=agent_result["is_business_related"],
                        knowledge_gap_detected=agent_result["knowledge_gap_detected"],
                        sentiment=agent_result["sentiment"]
                    ),
                )
            )
            
            self.logger.info("Insert agent analytics data is successfully")
            return UseCaseResult.success_result(
                MessageProcessingUseCaseOutput(
                    customer_id=customer.id,
                    text_message=agent_result["user_message"],
                    response=agent_result["response"],
                    detail_agent_output={
                        "handoff_reason": agent_result["handoff_reason"],
                        "fallback_human": agent_result["fallback_human"],
                        "confidence_level": agent_result["confidence_level"],
                    },
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while processing message usecase: {str(e)}", e
            )
