from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command
from src.whatsapp_agent.schema.business_context import BusinessContext
from .schema.review_handoff_schema import JudgeDecision
from .schema.review_handoff_schema import ReviewHumanHandoffInput
from .prompt import HumanHandoffPrompt
from src.whatsapp_agent.model import ContextAgent

class HumanHandoffService:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
    
    def _get_business_knowledge(self,business_context: BusinessContext | None) -> dict | None:
        if business_context is None or business_context.business_knowladge_content is None:
            return None
        business_knowladge = {}
        for k, v in business_context.business_knowladge_content.items():
            business_knowladge[k] = v.category_description
        
        return business_knowladge
    
    def _generate_advocate(self, handoff_reason: str, decision_summary: str, conversation_summary: str, business_knowladge: dict | None):
        prompt = HumanHandoffPrompt.advocate_agent(handoff_reason, decision_summary, conversation_summary, business_knowladge)
        result = self.model.invoke(prompt)
        return result.content
    
    def _generate_critic(self, handoff_reason: str, decision_summary: str, conversation_summary: str, business_knowladge: dict | None):

        prompt = HumanHandoffPrompt.critic_agent(handoff_reason, decision_summary, conversation_summary, business_knowladge)
        result = self.model.invoke(prompt)
        return result.content
    
    def generate_decision(self, handoff_reason: str, decision_summary: str, conversation_summary: str, business_context: BusinessContext | None):
        business_knowladge = self._get_business_knowledge(business_context)
        advocate_result = self._generate_advocate(handoff_reason, decision_summary, conversation_summary, business_knowladge)
        critic_result = self._generate_critic(handoff_reason, decision_summary, conversation_summary, business_knowladge)
        prompt = HumanHandoffPrompt.judge_agent(handoff_reason, decision_summary, conversation_summary, advocate_result, critic_result, business_knowladge)
        result = self.model.with_structured_output(JudgeDecision).invoke(prompt)
        return result

human_handoff_service = HumanHandoffService()

@tool(args_schema=ReviewHumanHandoffInput)
def review_human_handoff(handoff_reason: str, decision_summary: str, conversation_summary: str, runtime: ToolRuntime[ContextAgent]):
    """
    Review whether a human handoff is justified. The tool evaluates your reasoning and available business knowledge before recommending whether to escalate or continue using available tools.
    """
    business_context = runtime.state.business_context or None
    
    judge_decision = human_handoff_service.generate_decision(handoff_reason, decision_summary, conversation_summary, business_context)
    return Command(
        update={
            "fallback_human": judge_decision.handoff,
            "messages": ToolMessage(content=f"{judge_decision.justification}\n\nRECOMMENDATION:\n{judge_decision.recommendation or ""}", tool_call_id=runtime.tool_call_id),
            "skip_human_message": True
        }
    )