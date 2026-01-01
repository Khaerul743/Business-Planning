from typing import Any, Dict, Optional

from langchain_core.messages import AIMessage, HumanMessage

from src.infrastructure.ai.agent.base import BaseNode
from src.infrastructure.ai.agent.components.tools import RetrieveDocumentTool

from .models import WhatsappAgentState
from .prompts import SimpleRagPrompt


class SimpleRagAgentNodes(BaseNode):
    def __init__(
        self,
        prompt: SimpleRagPrompt,
        retrieve_document_tool: RetrieveDocumentTool,
        llm_model: str,
        llm_provider: str,
        use_long_memory: bool = False,
        user_memory_id: Optional[str] = None,
    ):
        super().__init__(llm_model, llm_provider, use_long_memory, user_memory_id)
        self.prompts = prompt
        self.retrieve_document_tool = retrieve_document_tool

    def _main_agent(self, state: WhatsappAgentState) -> Dict[str, Any]:
        prompt = self.prompts.main_agent(state.user_message)
        # all_previous_messages = self.get_all_previous_messages(state.messages)
        # messages: list[Any] = [prompt[0]] + list(all_previous_messages) + [prompt[1]]
        messages = self.get_prompt_setup(prompt, state.messages)

        response = self.call_llm_with_tool(
            messages, [self.retrieve_document_tool.read_document]
        )

        # response = self.call_llm(messages)
        if self._is_include_long_memory():
            message = [
                HumanMessage(content=state.user_message),
                AIMessage(content=response.content),
            ]
            self.memory.add_context(message)

        self.estimate_total_tokens(prompt, state.user_message, response.content)

        return {
            "messages": list(state.messages)
            + [HumanMessage(content=state.user_message)]
            + [response],
            "response": response.content,
        }

    def _answer_by_rag(self, state: WhatsappAgentState):
        tool_message = self.get_content_state_last_message(state.messages)
        # llm prompt
        prompt = self.prompts.agent_answer_rag_question(
            state.user_message, tool_message
        )

        # all_previous_messages = self.get_all_previous_messages(state.messages)
        # messages: list[Any] = [prompt[0]] + list(all_previous_messages) + [prompt[1]]
        messages = self.get_prompt_setup(prompt, state.messages)
        response = self.call_llm(messages)

        self.estimate_total_tokens(prompt, state.user_message, response.content)
        return {
            "messages": list(state.messages) + [response],
            "response": response.content,
        }
