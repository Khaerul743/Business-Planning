from typing import Literal

from langgraph.checkpoint.memory import MemorySaver

from src.infrastructure.ai.agent.base import BaseAgent
from src.infrastructure.ai.agent.components.tools import RetrieveDocumentTool

from .models import WhatsappAgentState
from .nodes import WhatsappAgentNode
from .prompts import WhatsappAgentPrompt
from .schema import (
    BusinessDetailInformation,
    BusinessKnowladgeContent,
    DocumentRagDetail,
)
from .workflow import WhatsappAgentWorkflow


class WhatsappAgent(BaseAgent):
    def __init__(
        self,
        chromadb_path: str,
        collection_name: str,
        llm_model: str,
        llm_provider: str,
        base_prompt: str,
        tone: Literal["friendly", "formal", "casual", "profesional"],
        business_detail_information: BusinessDetailInformation,
        business_knowladge: dict[str, BusinessKnowladgeContent],
        document_rag_detail: list[DocumentRagDetail] | None,
    ):
        self.retrieve_document = RetrieveDocumentTool(chromadb_path, collection_name)
        self.prompt = WhatsappAgentPrompt(
            base_prompt,
            business_knowladge,
            business_detail_information,
            document_rag_detail,
            tone,
        )
        self.checkpointer = MemorySaver()
        self.node = WhatsappAgentNode(
            self.prompt,
            llm_model,
            llm_provider,
            business_knowladge,
            self.retrieve_document,
        )
        self.workflow = WhatsappAgentWorkflow(self.checkpointer, self.node)
        super().__init__(self.node, self.workflow)
