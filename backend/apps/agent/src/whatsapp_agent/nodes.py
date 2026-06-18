import uuid
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.runtime import Runtime
from ..core.business_context_manager import BusinessContextManager
from ..core.agent_configuration_manager import AgentConfigurationManager
from src.base.base_node import BaseNode
from .prompts import WhatsappAgentPrompt
from .model import (
    WhatsappAgentState,
    ContextAgent,
    MainAgentOutput,
    MessageAnalysisOutput,
    create_call_preparation_tool_model,
    FinalResultOutput,
)
from src.components.tools import get_business_knowladge


class WhatsappAgentNode(BaseNode):
    def __init__(
        self,
        business_context_manager: BusinessContextManager,
        agent_configuration_manager: AgentConfigurationManager,
    ):
        self.wa_agent_prompt = WhatsappAgentPrompt()
        self.business_context_manager = business_context_manager
        self.agent_configuration_manager = agent_configuration_manager
        self.retry = 0
        super().__init__(__name__)

    async def get_context(
        self, state: WhatsappAgentState, runtime: Runtime[ContextAgent]
    ):
        configurable = runtime.context or {}
        business_id = configurable.get("business_id")
        agent_id = configurable.get("agent_id")
        if business_id is None or agent_id is None:
            raise RuntimeError("Business id or agent id not found")

        business_context = await self.business_context_manager.get_context(
            uuid.UUID(agent_id), uuid.UUID(business_id)
        )

        agent_config = await self.agent_configuration_manager.get(uuid.UUID(agent_id))

        return {"configuration": agent_config, "business_context": business_context}

    
    async def main_agent(self, state: WhatsappAgentState):
        if state.business_context is None or state.configuration is None:
            raise RuntimeError("Business context or agent configuration is None")
        main_prompt = self.wa_agent_prompt.main_llm(state.configuration, state.business_context, state.user_message)
        prompt_setup = self.get_prompt_setup(main_prompt, state.messages)
        result = await self.invoke_llm_with_tool("openai","gpt-4o-mini",0.7,prompt_setup, [get_business_knowladge])
        return {
            "messages": [HumanMessage(content=state.user_message), result]
        }

    def should_continue(self, state: WhatsappAgentState):
        last_message = state.messages[-1]
        print(f"State === {state}")
        if last_message.tool_calls:
            return "tool"
    
    async def response_with_tool_context(self, state: WhatsappAgentState):
        if state.business_context is None or state.configuration is None:
            raise RuntimeError("Business context or agent configuration is None")
        main_prompt = self.wa_agent_prompt.main_prompt(state.configuration.base_prompt or "", state.configuration.tone, state.business_context)
        prompt_setup = [SystemMessage(content=main_prompt)] + list(state.messages)
        response = await self.invoke_model("openai","gpt-4o-mini",0.7, prompt_setup) 
        return {
            "messages": response
        }
    
    # async def main_agent(self, state: WhatsappAgentState):
    #     if state.business_context is None or state.configuration is None:
    #         raise RuntimeError("Business context or agent configuration is None")

    #     main_prompt = WhatsappAgentPrompt.main_llm(
    #         state.configuration, state.business_context, state.user_message
    #     )
    #     prompt_setup = self.get_prompt_setup(main_prompt, state.messages)

    #     result = await self.invoke_llm_with_structured_output(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt_setup,
    #         MainAgentOutput,
    #     )

    #     result_dict = result.model_dump()

    #     if result_dict["need_more_information"]:
    #         return {
    #             "messages": list(state.messages)
    #             + [HumanMessage(content=state.user_message)],
    #             "response": result_dict["your_answer"],
    #             "confidence_level": result_dict["confidence"],
    #             "need_more_information": result_dict["need_more_information"],
    #             "human_fallback": result_dict["human_fallback"],
    #             "decision_summary": result_dict["decision_summary"],
    #             "reasoning_trace": result_dict["decision_summary"],
    #             # "conversation_summary": self.con_summary,
    #         }

    #     return {
    #         "response": result_dict["your_answer"],
    #         # "conversation_summary": self.con_summary,
    #         "confidence_level": result_dict["confidence"],
    #         "need_more_information": result_dict["need_more_information"],
    #         "human_fallback": result_dict["human_fallback"],
    #         "decision_summary": result_dict["decision_summary"],
    #         "messages": list(state.messages)
    #         + [HumanMessage(content=state.user_message)]
    #         + [
    #             AIMessage(
    #                 content=(
    #                     result_dict["your_answer"] if result_dict["your_answer"] else ""
    #                 )
    #             )
    #         ],
    #         "reasoning_trace": result_dict["decision_summary"],
    #     }

    # def main_agent_router(self, state: WhatsappAgentState):
    #     if state.need_more_information:
    #         return "next_router"
    #     return "next_to_message_analysis"

    # def next_router_temp_node(self, state: WhatsappAgentState):
    #     return

    # async def message_analysis(self, state: WhatsappAgentState):
    #     if state.business_context is None or state.configuration is None:
    #         raise RuntimeError("Business context or agent configuration is None")

    #     prompt = WhatsappAgentPrompt.message_analysis_prompt(
    #         state.business_context.business_detail_information,
    #         state.user_message,
    #         state.response,
    #     )
    #     result = await self.invoke_llm_with_structured_output(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt,
    #         MessageAnalysisOutput,
    #     )

    #     result_dict = result.model_dump()

    #     return {
    #         "category": result_dict["category"],
    #         "is_business_related": result_dict["is_business_related"],
    #         "knowledge_gap_detected": result_dict["knowledge_gap_detected"],
    #     }

    # def router(self, state: WhatsappAgentState):
    #     if state.need_more_information and state.confidence_level >= 50:
    #         return "next"
    #     if state.human_fallback and state.confidence_level < 50:
    #         return "human_fallback"
    #     return "end"

    # async def say_sorry(self, state: WhatsappAgentState):
    #     if state.configuration is None:
    #         raise RuntimeError("agent configuration is None")
    #     prompt = WhatsappAgentPrompt.say_sorry(
    #         state.configuration,
    #         state.user_message,
    #         state.response,
    #         state.decision_summary,
    #     )
    #     result = await self.invoke_model(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt,
    #     )

    #     return {"messages": list(state.messages) + [result], "response": result.content}

    # async def human_fallback(self, state: WhatsappAgentState):
    #     if state.configuration is None:
    #         raise RuntimeError("agent configuration is None")
    #     history_messages_str = self.history_messages_output(state.messages)
    #     prompt = WhatsappAgentPrompt.human_fallback(
    #         history_messages_str, state.confidence_level, state.decision_summary
    #     )
    #     result = await self.invoke_model(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt,
    #     )

    #     response = AIMessage(
    #         content="Baik saya telah menghubungi human customer support, jadi untuk sementara waktu saya harus meresponse pertanyaan customer sebisa mungkin sampai human customer support mengambil alih."
    #     )
    #     return {
    #         "decision_summary": result.content,
    #         "messages": list(state.messages) + [response],
    #         "response": response.content,
    #         "reasoning_trace": result.content,
    #     }

    # def update_state_after_main_agent(self, state: WhatsappAgentState):
    #     return {
    #         "messages": list(state.messages)
    #         + [AIMessage(content=state.decision_summary)]
    #     }

    # async def call_preparation_tool(self, state: WhatsappAgentState):
    #     if state.business_context is None or state.configuration is None:
    #         raise RuntimeError("Business context or agent configuration is None")

    #     prompt = WhatsappAgentPrompt.call_preparation_tool(
    #         state.business_context, state.user_message, state.decision_summary
    #     )

    #     if state.business_context.business_knowladge_content is None:
    #         raise RuntimeError("Business knowladge is None")
    #     business_knowladge_list = []
    #     for k, v in state.business_context.business_knowladge_content.items():
    #         business_knowladge_list.append(k)

    #     result = await self.invoke_llm_with_structured_output(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt,
    #         create_call_preparation_tool_model(business_knowladge_list),
    #     )

    #     result_dict = result.model_dump()
    #     return {
    #         "messages": list(state.messages)
    #         + [AIMessage(content=result_dict["decision_summary"])],
    #         "business_knowladge_key": result_dict["business_knowladge"],
    #         "rag_query": result_dict["rag_query"],
    #         "reasoning_trace": result_dict["decision_summary"],
    #     }

    # def get_business_knowladge(self, state: WhatsappAgentState):
    #     if (
    #         state.business_context is None
    #         or state.business_context.business_knowladge_content is None
    #     ):
    #         raise RuntimeError("Business context is None")
    #     if len(state.business_knowladge_key) == 0:
    #         return {"business_knowladge_result": None}
    #     list_content = ""
    #     for i in state.business_knowladge_key:
    #         list_content += f"key_{i}: {state.business_context.business_knowladge_content[i].content}\n"

    #     return {"business_knowladge_result": list_content}

    # def merge_tool_result(self, state: WhatsappAgentState):
    #     list_tool_result = []
    #     if state.rag_query_result:
    #         id_tool_1 = str(uuid.uuid4())
    #         list_tool_result.append(
    #             AIMessage(
    #                 content="Saya akan mengambil dokument untuk mendapatkan konteks tambahan",
    #                 tool_calls=[
    #                     {
    #                         "id": id_tool_1,
    #                         "name": "retrieve_document",
    #                         "args": {"query": state.rag_query},
    #                     }
    #                 ],
    #             )
    #         )

    #         list_tool_result.append(
    #             ToolMessage(content=state.rag_query_result, tool_call_id=id_tool_1)
    #         )

    #     if state.business_knowladge_result:
    #         id_tool_2 = str(uuid.uuid4())
    #         list_tool_result.append(
    #             AIMessage(
    #                 content="Saya akan mengambil business knowladge dengan key yang sesuai untuk mendapatkan konteks tambahan",
    #                 tool_calls=[
    #                     {
    #                         "id": id_tool_2,
    #                         "name": "retrieve_business_knowladge",
    #                         "args": {
    #                             "business_knowladge_key": state.business_knowladge_key
    #                         },
    #                     }
    #                 ],
    #             )
    #         )
    #         list_tool_result.append(
    #             ToolMessage(
    #                 content=state.business_knowladge_result,
    #                 tool_call_id=id_tool_2,
    #             )
    #         )

    #     return {
    #         "messages": list(state.messages) + list_tool_result,
    #     }

    # async def final_result(self, state: WhatsappAgentState):
    #     if state.business_context is None or state.configuration is None:
    #         raise RuntimeError("Business context or agent configuration is None")
    #     main_prompt = WhatsappAgentPrompt.main_llm(
    #         state.configuration, state.business_context, state.user_message
    #     )
    #     prompt_setup = self.get_prompt_setup(main_prompt, state.messages)
    #     result = await self.invoke_llm_with_structured_output(
    #         state.configuration.llm_provider,
    #         state.configuration.llm_model,
    #         state.configuration.temperature or 0.7,
    #         prompt_setup,
    #         FinalResultOutput,
    #     )
    #     result_dict = result.model_dump()

    #     return {
    #         "response": result_dict["your_answer"],
    #         "messages": list(state.messages)
    #         + [AIMessage(content=result_dict["your_answer"])],
    #         "decision_summary": result_dict["decision_summary"],
    #         "call_tool_again": result_dict["call_tool_again"],
    #         "human_fallback": result_dict["human_fallback"],
    #         "reasoning_trace": result_dict["decision_summary"],
    #     }

    # def final_result_router(self, state: WhatsappAgentState):
    #     if self.retry >= 3:
    #         self.retry = 0
    #         return "say_sorry"
    #     if state.call_tool_again and state.confidence_level >= 50:
    #         self.retry += 1
    #         return "next"
    #     if state.human_fallback and state.confidence_level < 50:
    #         return "human_fallback"
    #     return "message_analysis"
