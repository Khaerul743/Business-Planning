from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode

from src.infrastructure.ai.agent.base import BaseWorkflow

from .models import WhatsappAgentState
from .nodes import SimpleRagAgentNodes


class SimpleRagWorkflow(BaseWorkflow):
    def __init__(
        self,
        agent_node: SimpleRagAgentNodes,
        state_saver: BaseCheckpointSaver,
    ):
        self.nodes = agent_node
        self.checkpointer = state_saver
        self.build = self._build_workflow()

    def _build_workflow(
        self,
    ) -> CompiledStateGraph[
        WhatsappAgentState, None, WhatsappAgentState, WhatsappAgentState
    ]:
        if self.nodes is None:
            raise ValueError("Agent node must be set before building workflow")

        graph = StateGraph(WhatsappAgentState)
        graph.add_node("main_agent", self.nodes._main_agent)
        graph.add_node(
            "read_document",
            ToolNode(tools=[self.nodes.retrieve_document_tool.read_document]),
        )
        graph.add_node("answer_by_rag", self.nodes._answer_by_rag)

        graph.add_edge(START, "main_agent")
        graph.add_conditional_edges(
            "main_agent",
            self.nodes.conditional_tool_call,
            {"tool_call": "read_document", "end": END},
        )

        graph.add_edge("read_document", "answer_by_rag")
        graph.add_edge("answer_by_rag", END)

        return graph.compile(checkpointer=self.checkpointer)

    def run(self, state: WhatsappAgentState, thread_id: str):
        return self.build.invoke(
            state,
            config={"configurable": {"thread_id": thread_id}},
        )

    def show(self):
        pass
