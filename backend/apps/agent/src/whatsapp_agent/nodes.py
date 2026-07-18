import uuid
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from src.core.business_context_manager import BusinessContextManager
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.base.base_node import BaseNode
from .prompts import WhatsappAgentPrompt
from .model import (
    WhatsappAgentState,
    MessageAnalysisOutput,
)
from src.core.context_model import ContextAgent
from src.components.tools import get_business_knowladge, human_handoff, review_human_handoff


class WhatsappAgentNode(BaseNode):
    def __init__(
        self,
        business_context_manager: BusinessContextManager,
        agent_configuration_manager: AgentConfigurationManager,
    ):
        self.wa_agent_prompt = WhatsappAgentPrompt()
        self.business_context_manager = business_context_manager
        self.agent_configuration_manager = agent_configuration_manager
        self.retry = 0
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
            uuid.UUID(agent_id), uuid.UUID(business_id)
        )

        agent_config = await self.agent_configuration_manager.get(uuid.UUID(agent_id))

        return {
            "configuration": agent_config,
            "business_context": business_context,
            "fallback_human": False,
            "confidence_level": 100,
            "handoff_reason": "",
            "token_usage": 0
        }

    
    async def main_agent(self, state: WhatsappAgentState):
        if state.business_context is None or state.configuration is None:
            raise RuntimeError("Business context or agent configuration is None")
        
        if state.skip_human_message:
            main_prompt = self.wa_agent_prompt.main_llm(state.configuration, state.business_context, state.user_message)
            prompt_setup = [main_prompt[0]] + list(state.messages)
            result = await self.invoke_llm_with_tool("openai","gpt-4o-mini",0.7,prompt_setup, [get_business_knowladge, review_human_handoff, human_handoff])
            tokens = result.usage_metadata.get("total_tokens", 0) if hasattr(result, "usage_metadata") and result.usage_metadata else 0
            return {
                "messages": result,
                "skip_human_message": False,
                "response": result.content,
                "token_usage": state.token_usage + tokens
            }
        main_prompt = self.wa_agent_prompt.main_llm(state.configuration, state.business_context, state.user_message)
        prompt_setup = self.get_prompt_setup(main_prompt, state.messages)
        result = await self.invoke_llm_with_tool("openai","gpt-4o-mini",0.7,prompt_setup, [get_business_knowladge, review_human_handoff, human_handoff])
        tokens = result.usage_metadata.get("total_tokens", 0) if hasattr(result, "usage_metadata") and result.usage_metadata else 0
        return {
            "messages": [HumanMessage(content=state.user_message), result],
            "response": result.content,
            "token_usage": state.token_usage + tokens
        }

    def should_continue(self, state: WhatsappAgentState):
        last_message = state.messages[-1]
        if last_message.tool_calls:
            return "tool"
        return "message_analysis"
    
    async def message_analysis(self, state: WhatsappAgentState):
        if state.business_context is None or state.configuration is None:
            raise RuntimeError("Business context or agent configuration is None")    
        message_analysis_prompt = self.wa_agent_prompt.message_analysis_prompt(state.business_context.business_detail_information, state.user_message, state.response)
        result, tokens = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7,message_analysis_prompt, MessageAnalysisOutput)
        return {
            "category": result.category,
            "is_business_related": result.is_business_related,
            "knowledge_gap_detected": result.knowledge_gap_detected,
            "sentiment": result.sentiment,
            "token_usage": state.token_usage + tokens
        }