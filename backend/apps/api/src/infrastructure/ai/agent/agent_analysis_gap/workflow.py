from typing import Any, Dict

from src.infrastructure.ai.agent.base import BaseWorkflow
from .nodes import AgentAnalysisGapNode
from langgraph.graph import StateGraph, START, END
from .models import AgentAnalysisGapState


class AgentAnalysisGapWorkflow(BaseWorkflow):
    def __init__(self, node: AgentAnalysisGapNode):
        self.node = node
        self.build = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(AgentAnalysisGapState)
        graph.add_node("context_builder", self.node.context_builder)
        graph.add_node("insight_generator", self.node.insight_generator)
        graph.add_node("recommendation_generator", self.node.recommendation_generator)
        graph.add_edge(START, "context_builder")
        graph.add_conditional_edges(
            "context_builder",
            self.node.should_continue,
            {"next": "insight_generator", "end": END},
        )
        graph.add_edge("insight_generator", "recommendation_generator")
        graph.add_edge("recommendation_generator", END)
        return graph.compile()

    def run(self, state: AgentAnalysisGapState, thread_id: str) -> Dict[str, Any] | Any:
        return self.build.invoke(state)

    def show(self):
        pass
