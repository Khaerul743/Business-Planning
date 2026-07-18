from langgraph.graph import StateGraph, START, END
from src.core.context_model import ContextAgent
from .nodes import BusinessInsightNodes
from .model import BusinessInsightState

class BusinessInsightWorkflow:
    def __init__(self, nodes: BusinessInsightNodes):
        self.nodes = nodes
    
    def build(self):
        graph = StateGraph(BusinessInsightState, context_schema=ContextAgent)
        graph.add_node("get_business_context", self.nodes.get_business_context)
        graph.add_node("context_builder", self.nodes.context_builder)
        graph.add_node("insight_generator", self.nodes.insightGenerator)
        graph.add_node("recommendation_generator", self.nodes.recommdationGenerator)

        graph.add_edge(START, "get_business_context")
        graph.add_edge("get_business_context", "context_builder")
        graph.add_edge("context_builder", "insight_generator")
        graph.add_edge("insight_generator", "recommendation_generator")
        graph.add_edge("recommendation_generator", END)

        return graph.compile(name="business_insight_agent")