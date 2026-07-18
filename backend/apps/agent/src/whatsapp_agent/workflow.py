from langgraph.graph import StateGraph, START, END
from .nodes import WhatsappAgentNode
from .model import WhatsappAgentState
from langgraph.prebuilt import ToolNode
from src.components.tools import get_business_knowladge, human_handoff, review_human_handoff
from src.core.context_model import ContextAgent

class WhatsappAgentWorkflow:
    def __init__(self, nodes: WhatsappAgentNode):
        self.nodes = nodes

    def build(self):
        graph = StateGraph(WhatsappAgentState, context_schema=ContextAgent)
        graph.add_node("get_context", self.nodes.get_context)
        graph.add_node("main_agent", self.nodes.main_agent)
        graph.add_node("tool", ToolNode([get_business_knowladge, review_human_handoff, human_handoff]))
        graph.add_node("message_analysis", self.nodes.message_analysis)

        graph.add_edge(START, "get_context")
        graph.add_edge("get_context", "main_agent")
        graph.add_conditional_edges("main_agent",
            self.nodes.should_continue,
            {
                "tool": "tool",
                "message_analysis": "message_analysis"
            }
        )
        graph.add_edge("tool", "main_agent")
        graph.add_edge("message_analysis", END)

        return graph.compile(name="whatsapp_agent_graph")
