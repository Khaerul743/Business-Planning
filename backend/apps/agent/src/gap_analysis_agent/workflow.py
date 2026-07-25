from langgraph.graph import StateGraph, START, END
from src.core.context_model import ContextAgent
from .nodes import AgentAnalysisGapNodes
from .models import AgentAnalysisGapState

class GapAnalysisWorkflow:
    def __init__(self, nodes: AgentAnalysisGapNodes):
        self.nodes = nodes
    
    def build(self):
        graph = StateGraph(AgentAnalysisGapState, context_schema=ContextAgent)
        graph.add_node("get_business_context_gap", self.nodes.get_business_context_gap)
        graph.add_node("context_builder_gap", self.nodes.context_builder_gap)
        graph.add_node("insight_generator_gap", self.nodes.insight_generator_gap)
        graph.add_node("recommendation_generator_gap", self.nodes.recommendation_generator_gap)
        graph.add_edge(START, "get_business_context_gap")
        graph.add_edge("get_business_context_gap", "context_builder_gap")
        graph.add_conditional_edges(
            "context_builder_gap",
            self.nodes.should_continue,
            {"next": "insight_generator_gap", "end": END},
        )
        graph.add_edge("insight_generator_gap", "recommendation_generator_gap")
        graph.add_edge("recommendation_generator_gap", END)
        return graph.compile(name="agent_analysis_gap")