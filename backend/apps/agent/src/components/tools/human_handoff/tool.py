from langgraph.types import Command
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from src.whatsapp_agent.model import ContextAgent
from .schema.handoff_schema import HumanHandoffInput

@tool(args_schema=HumanHandoffInput)
def human_handoff(confidence_level: float, handoff_reason: str,decision_summary: str, runtime: ToolRuntime[ContextAgent]):
    """Untuk melakukan percakapan kepada admin manusia (human handoff)"""

    return Command(
        update={
            "messages": [ToolMessage(content="Human Handoff berhasil dilakukan", tool_call_id=runtime.tool_call_id)],
            "decision_summary": decision_summary,
            "confidence_level": confidence_level,
            "handoff_reason": handoff_reason,
            "skip_human_message": True,
            "token_usage": runtime.state.token_usage
        }
    )