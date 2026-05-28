from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.app.validators.analytic_schema import InsertAgentAnalytic
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAnalyticRepository
from src.infrastructure.ai.agent.base import BaseAgentStateModel
from src.infrastructure.ai.agent.manager import WhatsappAgentManager

from .create_agent_obj import CreateAgentObjInput, CreateAgentObjUseCase


@dataclass
class InvokeAgentInput:
    phone_number_id: str
    business_id: UUID
    agent_id: UUID
    thread_id: str
    agent_state: BaseAgentStateModel


@dataclass
class InvokeAgentOutput:
    text_message: str
    response: str
    detail_agent_output: dict


class InvokeAgentUseCase(BaseUseCase[InvokeAgentInput, InvokeAgentOutput]):
    def __init__(
        self,
        agent_analytic_repo: IAnalyticRepository,
        whatsapp_agent_manager: WhatsappAgentManager,
        craete_agent_obj_usecase: CreateAgentObjUseCase,
    ):
        self.agent_analytic_repo = agent_analytic_repo
        self.whatsapp_agent_manager = whatsapp_agent_manager
        self.craete_agent_obj_usecase = craete_agent_obj_usecase

    async def execute(
        self, input_data: InvokeAgentInput
    ) -> UseCaseResult[InvokeAgentOutput]:
        try:
            # Get agent from agent manager
            is_agent_exist = self.whatsapp_agent_manager.exists(
                input_data.phone_number_id
            )

            if not is_agent_exist:
                usecase_result = await self.craete_agent_obj_usecase.execute(
                    input_data=CreateAgentObjInput(
                        business_id=input_data.business_id,
                        phone_number_id=input_data.phone_number_id,
                        agent_id=input_data.agent_id,
                    )
                )
                agent_data = usecase_result.get_data()
                if agent_data is None:
                    return UseCaseResult.error_result(
                        "Unexpected error in create agent obj usecase",
                        usecase_result.get_exception(),
                    )
                agent = agent_data.agent
            else:
                agent = self.whatsapp_agent_manager.get_agent_by_phone_number_id(
                    input_data.phone_number_id
                )

            # Execute the agent
            agent_result = agent.execute(input_data.agent_state, input_data.thread_id)
            response_time = agent.get_response_time()
            result_response = agent.get_response()
            total_token = agent.get_token_usage()
            print(agent.show_execute_detail())
            result_message = (
                "Maaf, sepertinya sistem kami sedang ada gangguan. Mohon coba lagi nanti"
                if result_response is None
                else result_response
            )

            # # Insert Agent Analytic
            # date_now = datetime.now().date()

            # agent_analytic = await self.agent_analytic_repo.insert_agent_analytic(
            #     input_data.agent_id,
            #     InsertAgentAnalytic(
            #         date=str(date_now),
            #         total_message=2,
            #         response_time=response_time,
            #         token=total_token,
            #         ai_response=result_message,
            #         human_takeover=agent_result["human_fallback"],
            #         user_message=input_data.agent_state.user_message,
            #         category=agent_result["category"],
            #         is_business_related=agent_result["is_business_related"],
            #         knowledge_gap_detected=agent_result["knowledge_gap_detected"],
            #     ),
            # )

            return UseCaseResult.success_result(
                InvokeAgentOutput(
                    text_message=input_data.agent_state.user_message,
                    response=result_message,
                    detail_agent_output={
                        "decision_summary": agent_result["decision_summary"],
                        "human_fallback": agent_result["human_fallback"],
                        "confidence_level": agent_result["confidence_level"],
                    },
                )
            )

        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while invoke usecase: {str(e)}", e
            )
