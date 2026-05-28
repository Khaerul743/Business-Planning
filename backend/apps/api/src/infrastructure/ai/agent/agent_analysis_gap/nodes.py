from src.infrastructure.ai.agent.base import BaseNode
from .prompts import AgentAnalysisGapPrompt
from .models import (
    AgentAnalysisGapState,
    ContextBuilderStructuredOutput,
    InsigtGeneratorStructuredOutput,
)


class AgentAnalysisGapNode(BaseNode):
    def __init__(self, prompt: AgentAnalysisGapPrompt):
        self.prompt = prompt
        super().__init__(llm_model="gpt-4o-mini", provider="openai")

    def context_builder(self, state: AgentAnalysisGapState):
        prompt = self.prompt.context_builder_prompt(
            state.business_description, state.raw_data
        )
        result = self.call_llm_with_structured_output(
            prompt, ContextBuilderStructuredOutput
        )
        result_dict = result.model_dump()
        return {
            "is_gap_knowladge": result_dict["is_gap_knowladge"],
            "insight_context": result_dict["insight_context"],
        }

    def should_continue(self, state: AgentAnalysisGapState):
        if state.is_gap_knowladge:
            return "next"
        return "end"

    def insight_generator(self, state: AgentAnalysisGapState):
        prompt = self.prompt.insight_generator_prompt(
            state.business_description, state.insight_context
        )
        result = self.call_llm_with_structured_output(
            prompt, InsigtGeneratorStructuredOutput
        )
        result_dict = result.model_dump()
        return {
            "insight": result_dict["insight"],
            "knowladge_business_gap": result_dict["knowladge_business_gap"],
        }

    def recommendation_generator(self, state: AgentAnalysisGapState):
        prompt = self.prompt.recommendation_generator_prompt(
            state.business_description, state.insight, state.knowladge_business_gap
        )
        result = self.call_llm(prompt)
        return {"recommendation": result.content}
