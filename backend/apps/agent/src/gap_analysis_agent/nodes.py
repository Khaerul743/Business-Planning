from typing import Any
from uuid import UUID
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.core.context_model import ContextAgent
from src.base.base_node import BaseNode
from langgraph.runtime import Runtime
from .models import AgentAnalysisGapState, ContextBuilderStructuredOutput, InsigtGeneratorStructuredOutput, RecommendationOutput
from .prompts import AgentAnalysisGapPrompt


class AgentAnalysisGapNodes(BaseNode):
    def __init__(self, agent_configuration_manager):
        self.agent_configuration_manager = agent_configuration_manager

        super().__init__(__name__)

    async def get_business_context(
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
    
    async def context_builder(self,state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        prompt = AgentAnalysisGapPrompt.context_builder_prompt(state.business_description, state.raw_data)
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, ContextBuilderStructuredOutput)
        print("HELOOOOOOOOOOOOOO================================")
        return {
            "is_gap_knowladge": response.is_gap_knowladge,
            "insight_context": response.insight_context,
        }
    
    def should_continue(self, state: AgentAnalysisGapState):
        if state.is_gap_knowladge:
            return "next"
        return "end"
    
    def _normalize_text_content(self, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, list):
            return "\n".join(
                getattr(item, "content", str(item)) for item in value
            )
        return str(value)

    async def insight_generator(self, state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        prompt = AgentAnalysisGapPrompt.insight_generator_prompt(state.business_description, state.insight_context)
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, InsigtGeneratorStructuredOutput)

        return {
            "insight": self._normalize_text_content(response.insight),
            "knowladge_business_gap": self._normalize_text_content(response.knowladge_business_gap),
        }

    async def recommendation_generator(self, state: AgentAnalysisGapState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        insight = self._normalize_text_content(state.insight)
        knowladge_business_gap = self._normalize_text_content(state.knowladge_business_gap)
        prompt = AgentAnalysisGapPrompt.recommendation_generator_prompt(
            state.business_description,
            insight,
            knowladge_business_gap,
        )
        response, token = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.7, prompt, RecommendationOutput)

        return {
            "recommendation": self._normalize_text_content(response.recommendation)
        }