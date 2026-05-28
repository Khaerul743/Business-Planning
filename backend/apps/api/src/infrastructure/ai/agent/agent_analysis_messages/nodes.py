from src.infrastructure.ai.agent.base import BaseNode
from .prompts import AgentAnalysisPrompt
from .models import AgentAnalysisState, InsightGeneratorOutput


class AgentAnalysisNode(BaseNode):
    def __init__(self, prompts: AgentAnalysisPrompt, llm_model: str, llm_provider: str):
        self.prompts = prompts
        super().__init__(llm_model, llm_provider)

    def contextBuilder(self, state: AgentAnalysisState):
        prompts = self.prompts.context_builder_prompt(
            state.business_description, state.raw_data
        )
        result = self.call_llm(prompts)
        self.estimate_total_tokens(prompts, "", result.content)
        return {"insight_context": result.content}

    def insightGenerator(self, state: AgentAnalysisState):
        prompts = self.prompts.insight_generator(
            state.business_description, state.insight_context
        )
        result = self.call_llm_with_structured_output(prompts, InsightGeneratorOutput)
        result_dict = result.model_dump()
        return {
            "insight": result_dict["insight"],
            "reason": result_dict["reason"],
            "impact": result_dict["impact"],
        }

    def recommendationGenerator(self, state: AgentAnalysisState):
        prompts = self.prompts.recommendation_generator(
            state.business_description, state.insight, state.reason, state.impact
        )
        result = self.call_llm(prompts)
        return {"recommendation": result.content}
