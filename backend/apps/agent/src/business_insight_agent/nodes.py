from uuid import UUID
from langgraph.runtime import Runtime
from src.core.agent_configuration_manager import AgentConfigurationManager
from src.core.context_model import ContextAgent
from src.base.base_node import BaseNode
from .prompts import BusinessInsightPrompt
from .model import BusinessInsightState, InsightGeneratorOutput, RecommendationOutput

class BusinessInsightNodes(BaseNode):
    def __init__(self, agent_configuration_manager):
        self.agent_configuration_manager = agent_configuration_manager

    async def get_business_context(
        self, state: BusinessInsightState, runtime: Runtime[ContextAgent]
    ):
        configurable = runtime.context or {}
        agent_id = configurable.get("agent_id")
        if agent_id is None:
            raise RuntimeError("Business id or agent id not found")

        agent_config = await self.agent_configuration_manager.get(UUID(agent_id))

        return {
            "configuration": agent_config,
        }
    
    async def context_builder(self, state: BusinessInsightState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        prompt = BusinessInsightPrompt.context_builder_prompt(state.business_description, state.raw_data)
        response = await self.invoke_model(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.5, prompt)
        return {
            "insight_context": response.content
        }
    
    async def insightGenerator(self, state: BusinessInsightState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.")
        
        prompt = BusinessInsightPrompt.insight_generator(state.business_description, state.insight_context)
        response = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.5, prompt, InsightGeneratorOutput)
        result_dict = response.model_dump()
        return {
            "insight": result_dict["insight"],
            "reason": result_dict["reason"],
            "impact": result_dict["impact"],
        }
    
    async def recommdationGenerator(self, state: BusinessInsightState):
        if state.configuration is None:
            raise RuntimeError("Agent configuration not found.") 
        prompt = BusinessInsightPrompt.recommendation_generator(state.business_description, state.insight, state.reason, state.impact)
        response = await self.invoke_llm_with_structured_output(state.configuration.llm_provider, state.configuration.llm_model, state.configuration.temperature or 0.5, prompt, RecommendationOutput)
        result_dict = response.model_dump()
        return {
            "recommendation": result_dict["recommendation"]
        }