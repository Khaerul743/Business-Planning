from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from src.core.context_model import ContextAgent
from src.whatsapp_agent.schema.business_context import BusinessContext
from .schema.get_business_knowladge import BusinessKnowladgeInput
from .schema.output_schema import create_gathering_knowledge_output
from .prompts import ToolPrompt

class BusinessKnowladgeTool:
    def __init__(self):
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
    
    def _get_business_knowledge_key(self,business_context: BusinessContext) -> list[str]:
        if business_context.business_knowladge_content is None:
            raise RuntimeError("Business knowladge is None")
        business_knowladge_list = []
        for k, v in business_context.business_knowladge_content.items():
            business_knowladge_list.append(k)
        
        return business_knowladge_list
    
    def gathering_knowledge(self, business_context: BusinessContext, query: str, conversation_context: str):
        if business_context.business_knowladge_content is None:
            raise RuntimeError("Business knowladge is None") 
        
        prompt = ToolPrompt.gathering_knowledge(business_context, query, conversation_context)
        business_knowladge_key = self._get_business_knowledge_key(business_context)

        result_dict = self.model.with_structured_output(create_gathering_knowledge_output(business_knowladge_key), include_raw=True).invoke(prompt)
        result = result_dict["parsed"]
        raw = result_dict["raw"]
        tokens = raw.usage_metadata.get("total_tokens", 0) if hasattr(raw, "usage_metadata") and raw.usage_metadata else 0
        rag_query = result.rag_query
        business_knowladge_key_choosed = result.business_knowladge

        business_knowladge_result = []
        for i in business_knowladge_key_choosed:
            business_knowladge_result.append(business_context.business_knowladge_content[i].content)

        #RAG HERE

        return f"BUSINESS KNOWLEDGE: \n {'\n'.join(business_knowladge_result)}", tokens

business_knowladge_service = BusinessKnowladgeTool()

@tool(args_schema=BusinessKnowladgeInput)
def get_business_knowladge(query: str, conversation_context: str, decision_summary: str, runtime: ToolRuntime[ContextAgent]):
    """Untuk mengambil informasi terkait dengan bisnis/perusahaan"""
    business_context = runtime.state.business_context or None
    if business_context is None:
        return "Tidak ada business knowladge yang tersedia."
        
    knowledge, tokens = business_knowladge_service.gathering_knowledge(business_context, query, conversation_context)
    return Command(
        update={
            "messages": [ToolMessage(content=knowledge, tool_call_id=runtime.tool_call_id)],
            "skip_human_message": True,
            "decision_summary": decision_summary,
            "token_usage": runtime.state.token_usage + tokens
        }
    )

