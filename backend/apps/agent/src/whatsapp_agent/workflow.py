from langgraph.graph import StateGraph, START, END
from .nodes import WhatsappAgentNode
from .model import WhatsappAgentState, ContextAgent
from langgraph.prebuilt import ToolNode
from src.components.tools import get_business_knowladge

class WhatsappAgentWorkflow:
    def __init__(self, nodes: WhatsappAgentNode):
        self.nodes = nodes

    def build(self):
        graph = StateGraph(WhatsappAgentState, context_schema=ContextAgent)
        graph.add_node("get_context", self.nodes.get_context)
        graph.add_node("main_agent", self.nodes.main_agent)
        graph.add_node("tool", ToolNode([get_business_knowladge]))
        graph.add_node("res_tool_context", self.nodes.response_with_tool_context)

        # graph.add_node(
        #     "update_state_aftet_main_agent", self.nodes.update_state_after_main_agent
        # )
        # graph.add_node("temp_node", self.nodes.next_router_temp_node)
        # graph.add_node("message_analysis", self.nodes.message_analysis)
        # graph.add_node("say_sorry", self.nodes.say_sorry)
        # graph.add_node("human_fallback", self.nodes.human_fallback)
        # graph.add_node("get_business_knowladge", self.nodes.get_business_knowladge)
        # graph.add_node("merge_tool_result", self.nodes.merge_tool_result)
        # graph.add_node("final_result", self.nodes.final_result)

        # graph.add_node(
        #     "call_preparation_tool",
        #     self.nodes.call_preparation_tool,
        # )

        graph.add_edge(START, "get_context")
        graph.add_edge("get_context", "main_agent")
        graph.add_conditional_edges("main_agent",
            self.nodes.should_continue
        )
        graph.add_edge("tool", "res_tool_context")
        graph.add_edge("res_tool_context", END)

        # graph.add_conditional_edges(
        #     "main_agent",
        #     self.nodes.main_agent_router,
        #     {
        #         "next_router": "temp_node",
        #         "next_to_message_analysis": "message_analysis",
        #     },
        # )
        # graph.add_conditional_edges(
        #     "temp_node",
        #     self.nodes.router,
        #     {
        #         "end": END,
        #         "next": "update_state_aftet_main_agent",
        #         "human_fallback": "human_fallback",
        #     },
        # )
        # graph.add_edge("human_fallback", END)
        # graph.add_edge("say_sorry", END)
        # graph.add_edge("update_state_aftet_main_agent", "call_preparation_tool")
        # graph.add_edge("call_preparation_tool", "get_business_knowladge")

        # graph.add_edge(
        #     "get_business_knowladge",
        #     "merge_tool_result",
        # )

        # graph.add_edge("merge_tool_result", "final_result")
        # graph.add_conditional_edges(
        #     "final_result",
        #     self.nodes.final_result_router,
        #     {
        #         "say_sorry": "say_sorry",
        #         "next": "call_preparation_tool",
        #         "human_fallback": "human_fallback",
        #         "message_analysis": "message_analysis",
        #     },
        # )
        # graph.add_edge("message_analysis", END)
        return graph.compile(name="whatsapp_agent_graph")
