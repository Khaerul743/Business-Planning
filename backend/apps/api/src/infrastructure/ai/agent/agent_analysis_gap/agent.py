from src.infrastructure.ai.agent.base import BaseAgent
from .workflow import AgentAnalysisGapWorkflow
from .nodes import AgentAnalysisGapNode
from .prompts import AgentAnalysisGapPrompt


class AgentAnalysisGap(BaseAgent):
    def __init__(self):
        self.prompt = AgentAnalysisGapPrompt()
        self.node = AgentAnalysisGapNode(self.prompt)
        self.workflow = AgentAnalysisGapWorkflow(self.node)
        super().__init__(self.node, self.workflow)
