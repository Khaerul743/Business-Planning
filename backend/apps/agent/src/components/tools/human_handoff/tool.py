from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI
from .schema.handoff_schema import HumanHandoffInput, JudgeDecision
from .prompt import HumanHandoffPrompt

class HumanHandoffService:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
    
    def _generate_advocate(self, handoff_reason: str, decision_summary: str, conversation_summary: str):
        prompt = HumanHandoffPrompt.advocate_agent(handoff_reason, decision_summary, conversation_summary)
        result = self.model.invoke(prompt)
        return result.content
    
    def _generate_critic(self, handoff_reason: str, decision_summary: str, conversation_summary: str):
        prompt = HumanHandoffPrompt.critic_agent(handoff_reason, decision_summary, conversation_summary)
        result = self.model.invoke(prompt)
        return result.content
    
    def generate_decision(self, handoff_reason: str, decision_summary: str, conversation_summary: str):
        advocate_result = self._generate_advocate(handoff_reason, decision_summary, conversation_summary)
        critic_result = self._generate_critic(handoff_reason, decision_summary, conversation_summary)
        prompt = HumanHandoffPrompt.judge_agent(handoff_reason, decision_summary, conversation_summary, advocate_result, critic_result)
        result = self.model.with_structured_output(JudgeDecision).invoke(prompt)
        return result

human_handoff_service = HumanHandoffService()

@tool(args_schema=HumanHandoffInput)
def human_handoff(confidence_level: float, handoff_reason: str, decision_summary: str, conversation_summary: str):
    """Untuk mengalihkan conversation kepada human admin"""
    judge_decision = human_handoff_service.generate_decision(handoff_reason, decision_summary, conversation_summary)
    