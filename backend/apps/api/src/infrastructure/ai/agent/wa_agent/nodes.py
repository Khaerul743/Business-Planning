import uuid
from typing import Optional, Sequence

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage

from src.infrastructure.ai.agent.base import BaseNode
from src.infrastructure.ai.agent.components.tools import RetrieveDocumentTool

from .models import (
    FinalResultOutput,
    MainAgentOutput,
    WhatsappAgentState,
    create_call_preparation_tool_model,
    MessageAnalysisOutput,
)
from .prompts import WhatsappAgentPrompt
from .schema import BusinessKnowladgeContent


class WhatsappAgentNode(BaseNode):
    def __init__(
        self,
        prompt: WhatsappAgentPrompt,
        llm_model: str,
        llm_provider: str,
        business_knowladge: dict[str, BusinessKnowladgeContent],
        retrieve_document: RetrieveDocumentTool,
        use_long_memory: bool = False,
    ):
        self.prompt = prompt
        self.business_knowladge = business_knowladge
        self.retrieve_document = retrieve_document
        self.business_knowladge_list = []
        for k, v in business_knowladge.items():
            self.business_knowladge_list.append(k)

        self.retry = 0
        self.MAX_MESSAGES = 10
        self.last_len_messages = 0
        self.con_repeat = 0
        self.con_summary = None
        super().__init__(llm_model, llm_provider, use_long_memory)

    def _create_conversation_summary(
        self, state_messages, con_summary: Optional[str] = None
    ):
        history_message_str = self._history_message_process(state_messages)
        messages = self.prompt.conversation_summary(history_message_str, con_summary)
        result = self.call_llm(messages)
        return result.content

    def main_agent(self, state: WhatsappAgentState):
        if self.con_repeat == 5:
            self.con_repeat = 0
            len_messages = len(state.messages)
            self.con_summary = self._create_conversation_summary(
                state.messages[self.last_len_messages : len_messages],
                state.conversation_summary,
            )
            self.last_len_messages = len_messages

        messages = self.get_prompt_setup(
            self.prompt.main_llm(state.user_message), state.messages, self.MAX_MESSAGES
        )
        try:
            result = self.call_llm_with_structured_output(messages, MainAgentOutput)
        except Exception:
            messages = self.get_prompt_setup(
                self.prompt.main_llm(state.user_message),
                state.messages,
                self.MAX_MESSAGES + 6,
            )
            result = self.call_llm_with_structured_output(messages, MainAgentOutput)

        result_dict = result.model_dump()

        # Count token usage
        self.estimate_structured_output_tokens(
            messages,
            str(
                result_dict["your_answer"] or "" + result_dict["decision_summary"] or ""
            ),
        )

        # conversation repeat
        self.con_repeat += 1
        if result_dict["need_more_information"]:
            return {
                "messages": list(state.messages)
                + [HumanMessage(content=state.user_message)],
                "response": result_dict["your_answer"],
                "confidence_level": result_dict["confidence"],
                "need_more_information": result_dict["need_more_information"],
                "human_fallback": result_dict["human_fallback"],
                "decision_summary": result_dict["decision_summary"],
                "conversation_summary": self.con_summary,
            }
        return {
            "response": result_dict["your_answer"],
            "conversation_summary": self.con_summary,
            "confidence_level": result_dict["confidence"],
            "need_more_information": result_dict["need_more_information"],
            "human_fallback": result_dict["human_fallback"],
            "decision_summary": result_dict["decision_summary"],
            "messages": list(state.messages)
            + [HumanMessage(content=state.user_message)]
            + [
                AIMessage(
                    content=(
                        result_dict["your_answer"] if result_dict["your_answer"] else ""
                    )
                )
            ],
        }

    def main_agent_router(self, state: WhatsappAgentState):
        if state.need_more_information:
            return "next_router"
        return "next_to_message_analysis"

    def next_router_temp_node(self, state: WhatsappAgentState):
        return

    def message_analysis(self, state: WhatsappAgentState):
        prompt = self.prompt.message_analysis_prompt(state.user_message, state.response)
        result = self.call_llm_with_structured_output(prompt, MessageAnalysisOutput)
        result_dict = result.model_dump()
        self.estimate_structured_output_tokens(
            prompt,
            str(result_dict["category"]),
        )
        return {
            "category": result_dict["category"],
            "is_business_related": result_dict["is_business_related"],
            "knowledge_gap_detected": result_dict["knowledge_gap_detected"],
        }

    def router(self, state: WhatsappAgentState):
        if state.need_more_information and state.confidence_level >= 50:
            return "next"
        if state.human_fallback and state.confidence_level < 50:
            return "human_fallback"
        return "end"

    def say_sorry(self, state: WhatsappAgentState):
        messages = self.prompt.say_sorry(
            state.user_message,
            state.response,
            state.decision_summary,
            state.conversation_summary,
        )
        result = self.call_llm(messages)

        # Count token usage
        self.estimate_total_tokens(messages, state.user_message, result.content)
        return {"messages": list(state.messages) + [result], "response": result.content}

    def _history_message_process(self, history_messages: Sequence[BaseMessage]):
        history_messages_str = ""
        for i in history_messages:
            if isinstance(i, HumanMessage):
                history_messages_str += f"*Customer*\n{i.content}\n\n"
            elif isinstance(i, AIMessage):
                history_messages_str += f"*AI*\n{i.content}\n\n"
            elif isinstance(i, ToolMessage):
                history_messages_str += f"*Tool Message*\n{i.content}\n\n"

        return history_messages_str

    def human_fallback(self, state: WhatsappAgentState):
        list_messages = state.messages
        history_messages_str = self._history_message_process(list_messages)
        last_decision_summary = state.decision_summary
        confidence_level = state.confidence_level
        messages = self.prompt.human_fallback(
            history_messages_str,
            confidence_level,
            last_decision_summary,
            state.conversation_summary,
        )

        result = self.call_llm(messages)

        # Count token usage
        self.estimate_total_tokens(messages, state.user_message, result.content)

        response = AIMessage(
            content="Baik saya telah menghubungi human customer support, jadi untuk sementara waktu saya harus meresponse pertanyaan customer sebisa mungkin sampai human customer support mengambil alih."
        )
        return {
            "decision_summary": result.content,
            "messages": list(state.messages) + [response],
            "response": response.content,
        }

    def update_state_after_main_agent(self, state: WhatsappAgentState):
        return {
            "messages": list(state.messages)
            + [AIMessage(content=state.decision_summary)]
        }

    def call_preparation_tool(self, state: WhatsappAgentState):
        # messages = self.get_prompt_setup(
        #     self.prompt.call_preparation_tool(state.user_message), state.messages
        # )
        messages = self.prompt.call_preparation_tool(state.user_message)
        result = self.call_llm_with_structured_output(
            messages, create_call_preparation_tool_model(self.business_knowladge_list)
        )
        result_dict = result.model_dump()
        # Count token usage
        self.estimate_structured_output_tokens(
            messages, str(result_dict["decision_summary"])
        )

        return {
            "messages": list(state.messages)
            + [AIMessage(content=result_dict["decision_summary"])],
            "business_knowladge_key": result_dict["business_knowladge"],
            "rag_query": result_dict["rag_query"],
        }

    def get_business_knowladge(self, state: WhatsappAgentState):
        if len(state.business_knowladge_key) == 0:
            return {"business_knowladge_result": None}
        list_content = ""
        for i in state.business_knowladge_key:
            list_content += f"key_{i}: {self.business_knowladge[i].content}\n"

        return {"business_knowladge_result": list_content}

    def get_rag_query(self, state: WhatsappAgentState):
        if not state.rag_query or state.rag_query == "":
            return {"rag_query_result": None}

        tool_result = self.retrieve_document.read_document(state.rag_query)
        return {"rag_query_result": tool_result}

    def merge_tool_result(self, state: WhatsappAgentState):
        list_tool_result = []
        if state.rag_query_result:
            id_tool_1 = str(uuid.uuid4())
            list_tool_result.append(
                AIMessage(
                    content="Saya akan mengambil dokument untuk mendapatkan konteks tambahan",
                    tool_calls=[
                        {
                            "id": id_tool_1,
                            "name": "retrieve_document",
                            "args": {"query": state.rag_query},
                        }
                    ],
                )
            )

            list_tool_result.append(
                ToolMessage(content=state.rag_query_result, tool_call_id=id_tool_1)
            )

        if state.business_knowladge_result:
            id_tool_2 = str(uuid.uuid4())
            list_tool_result.append(
                AIMessage(
                    content="Saya akan mengambil business knowladge dengan key yang sesuai untuk mendapatkan konteks tambahan",
                    tool_calls=[
                        {
                            "id": id_tool_2,
                            "name": "retrieve_business_knowladge",
                            "args": {
                                "business_knowladge_key": state.business_knowladge_key
                            },
                        }
                    ],
                )
            )
            list_tool_result.append(
                ToolMessage(
                    content=state.business_knowladge_result,
                    tool_call_id=id_tool_2,
                )
            )

        return {"messages": list(state.messages) + list_tool_result}

    def final_result(self, state: WhatsappAgentState):
        messages = self.get_prompt_setup(
            self.prompt.main_llm(state.user_message, state.conversation_summary),
            state.messages,
            self.MAX_MESSAGES,
        )
        try:
            result = self.call_llm_with_structured_output(messages, FinalResultOutput)
        except Exception:
            messages = self.get_prompt_setup(
                self.prompt.main_llm(state.user_message),
                state.messages,
                self.MAX_MESSAGES + 6,
            )
            result = self.call_llm_with_structured_output(messages, FinalResultOutput)

        result_dict = result.model_dump()

        # Count token usage
        self.estimate_structured_output_tokens(
            messages,
            str(
                result_dict["your_answer"] or "" + result_dict["decision_summary"] or ""
            ),
        )
        return {
            "response": result_dict["your_answer"],
            "messages": list(state.messages)
            + [AIMessage(content=result_dict["your_answer"])],
            "decision_summary": result_dict["decision_summary"],
            "call_tool_again": result_dict["call_tool_again"],
            "human_fallback": result_dict["human_fallback"],
        }

    def final_result_router(self, state: WhatsappAgentState):
        if self.retry >= 3:
            self.retry = 0
            return "say_sorry"
        if state.call_tool_again and state.confidence_level >= 50:
            self.retry += 1
            return "next"
        if state.human_fallback and state.confidence_level < 50:
            return "human_fallback"
        return "message_analysis"
