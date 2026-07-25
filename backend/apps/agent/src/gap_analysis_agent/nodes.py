from typing import Any
from uuid import UUID
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.core.context_model import ContextAgent
from src.base.base_node import BaseNode
from langgraph.runtime import Runtime
from .models import AgentAnalysisGapState, ContextBuilderStructuredOutput, InsigtGeneratorStructuredOutput, RecommendationOutput
from .prompts import AgentAnalysisGapPrompt


class AgentAnalysisGapNodes(BaseNode):
    def __init__(self, agent_configuration_manager: AgentConfigurationManager):
        self.agent_configuration_manager = agent_configuration_manager

        super().__init__(__name__)

    async def get_business_context_gap(
        self, state: AgentAnalysisGapState, runtime: Runtime[ContextAgent]
    ):
        configurable = runtime.context or {}
        agent_id = configurable.get("agent_id")
        if agent_id is None:
            raise RuntimeError("Business id or agent id not found")

        agent_config = await self.agent_configuration_manager.get(UUID(agent_id))
        return {
            "configuration": agent_config,
        }
    
    async def context_builder_gap(self,state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        
        prompt = AgentAnalysisGapPrompt.context_builder_prompt(state.business_description, state.raw_data)
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, ContextBuilderStructuredOutput)
        # response, token = await self.invoke_llm_with_structured_output("openai", "gpt-4o-mini",0.7, prompt, ContextBuilderStructuredOutput)
        return {
            "is_gap_knowladge": response.is_gap_knowladge,
            "insight_context": response.insight_context,
        }
    
    def should_continue(self, state: AgentAnalysisGapState):
        if state.is_gap_knowladge:
            return "next"
        return "end"
    
    # def _normalize_text_content(self, value: Any) -> str | None:
    #     if value is None:
    #         return None
    #     if isinstance(value, list):
    #         return "\n".join(
    #             getattr(item, "content", str(item)) for item in value
    #         )
    #     return str(value)

    async def insight_generator_gap(self, state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        prompt = AgentAnalysisGapPrompt.insight_generator_prompt(state.business_description, state.insight_context)
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, InsigtGeneratorStructuredOutput)
        # response, token = await self.invoke_llm_with_structured_output("openai", "gpt-4o-mini",0.7, prompt, ContextBuilderStructuredOutput)
        return {
            "insight": response.insight,
            "knowladge_business_gap": response.knowladge_business_gap,
        }

    async def recommendation_generator_gap(self, state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        insight = state.insight
        knowladge_business_gap = state.knowladge_business_gap
        prompt = AgentAnalysisGapPrompt.recommendation_generator_prompt(
            state.business_description,
            insight,
            knowladge_business_gap,
        )
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, RecommendationOutput)

        return {
            "recommendation": response.recommendation
        }