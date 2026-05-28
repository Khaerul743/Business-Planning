from src.infrastructure.ai.agent.base import BaseWorkflow
from langgraph.graph import END, START, StateGraph
from .nodes import AgentAnalysisNode
from .models import AgentAnalysisState


class AgentAnalysisWorklow(BaseWorkflow):
    def __init__(self, node: AgentAnalysisNode):
        self.node = node
        self.build = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(AgentAnalysisState)
        graph.add_node("context_builder", self.node.contextBuilder)
        graph.add_node("insight_generator", self.node.insightGenerator)
        graph.add_node("recommendation_generator", self.node.recommendationGenerator)

        graph.add_edge(START, "context_builder")
        graph.add_edge("context_builder", "insight_generator")
        graph.add_edge("insight_generator", "recommendation_generator")
        graph.add_edge("recommendation_generator", END)

        return graph.compile()

    def run(self, state: AgentAnalysisState, thread_id: str):
        return self.build.invoke(state)

    def show(self):
        pass
