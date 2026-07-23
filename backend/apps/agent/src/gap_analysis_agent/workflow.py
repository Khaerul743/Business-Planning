from langgraph.graph import StateGraph, START, END
from src.core.context_model import ContextAgent
from .nodes import AgentAnalysisGapNodes
from .models import AgentAnalysisGapState

class GapAnalysisWorkflow:
    def __init__(self, nodes: AgentAnalysisGapNodes):
        self.nodes = nodes
    
    def build(self):
        graph = StateGraph(AgentAnalysisGapState, context_schema=ContextAgent)
        graph.add_node("context_builder", self.nodes.context_builder)
        graph.add_node("insight_generator", self.nodes.insight_generator)
        graph.add_node("recommendation_generator", self.nodes.recommendation_generator)
        graph.add_edge(START, "context_builder")
        graph.add_conditional_edges(
            "context_builder",
            self.nodes.should_continue,
            {"next": "insight_generator", "end": END},
        )
        graph.add_edge("insight_generator", "recommendation_generator")
        graph.add_edge("recommendation_generator", END)
        return graph.compile(name="agent_analysis_gap")