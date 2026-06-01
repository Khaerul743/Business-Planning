from uuid import UUID
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from .utils.business_context_manager import BusinessContextManager
from .utils.agent_configuration_manager import AgentConfigurationManager
from src.base.base_node import BaseNode
from .prompts import WhatsappAgentPrompt
from .model import WhatsappAgentState, ContextAgent


class WhatsappAgentNode(BaseNode):
    def __init__(
        self,
        business_context_manager: BusinessContextManager,
        agent_configuration_manager: AgentConfigurationManager,
    ):
        self.business_context_manager = business_context_manager
        self.agent_configuration_manager = agent_configuration_manager

        super().__init__(__name__)

    async def get_context(
        self, state: WhatsappAgentState, runtime: Runtime[ContextAgent]
    ):
        configurable = runtime.context or {}
        business_id = configurable.get("business_id")
        agent_id = configurable.get("agent_id")
        if business_id is None or agent_id is None:
            raise RuntimeError("Business id or agent id not found")

        business_context = await self.business_context_manager.get_context(
            UUID(agent_id), UUID(business_id)
        )

        agent_config = await self.agent_configuration_manager.get(UUID(agent_id))

        return {"configuration": agent_config, "business_context": business_context}
