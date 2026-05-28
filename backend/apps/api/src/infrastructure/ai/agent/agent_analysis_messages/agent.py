from src.infrastructure.ai.agent.base import BaseAgent
from .prompts import AgentAnalysisPrompt
from .nodes import AgentAnalysisNode
from .workflow import AgentAnalysisWorklow


class AgentAnalysisMessages(BaseAgent):
    def __init__(self):
        self.prompts = AgentAnalysisPrompt()
        self.nodes = AgentAnalysisNode(self.prompts, "gpt-4o-mini", "openai")
        self.workflow = AgentAnalysisWorklow(self.nodes)

        super().__init__(self.nodes, self.workflow)
