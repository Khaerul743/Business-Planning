from langgraph.graph import StateGraph, START, END
from .nodes import WhatsappAgentNode
from .model import WhatsappAgentState, ContextAgent


class WhatsappAgentWorkflow:
    def __init__(self, nodes: WhatsappAgentNode):
        self.nodes = nodes

    def build(self):
        graph = StateGraph(WhatsappAgentState, context_schema=ContextAgent)
        graph.add_node("get_context", self.nodes.get_context)

        graph.add_edge(START, "get_context")
        graph.add_edge("get_context", END)

        return graph.compile(name="whatsapp_agent_graph")
