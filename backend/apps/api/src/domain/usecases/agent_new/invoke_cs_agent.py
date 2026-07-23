import httpx
from dataclasses import dataclass
from uuid import UUID

from src.core.exceptions.agent_exception import AgentNotFound
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IAgentRepository
from src.infrastructure.langgraph_server import langgraph_client, CustomerServiceAgentConfig

@dataclass
class InvokeCSAgentInput:
    agent_id: UUID
    thread_id: str
    text_message: str

@dataclass
class InvokeCSAgentOutput:
    result: dict

class InvokeCSAgent(BaseUseCase[InvokeCSAgentInput, InvokeCSAgentOutput]):
    def __init__(self, agent_repo: IAgentRepository):
        self.agent_repo = agent_repo

        super().__init__(__name__)
    async def execute(self, input_data: InvokeCSAgentInput) -> UseCaseResult[InvokeCSAgentOutput]:
        try:
            agent = await self.agent_repo.get_agent_by_id(input_data.agent_id)
            if agent is None:
                return UseCaseResult.error_result("Agent not found", AgentNotFound())   

            business_id = agent.business_id
            config = CustomerServiceAgentConfig(business_id=str(business_id), agent_id=str(input_data.agent_id))

            try:
                result = await langgraph_client.run_customer_service_agent(input_data.thread_id, config, input_data.text_message)  
            except httpx.HTTPStatusError as exc:
                self.logger.error(f"Error while run customer service agent: {exc}")
                self.logger.info(f"Registered new thread id")
                await langgraph_client.register_thread_id(UUID(input_data.thread_id))
                self.logger.info(f"Re-run customer service agent")
                result = await langgraph_client.run_customer_service_agent(input_data.thread_id, config, input_data.text_message)  
            
            return UseCaseResult.success_result(result)
        except Exception as e:
            return UseCaseResult.error_result(f"Unexpected error while invoke customer service agent usecase: {e}", e)
    