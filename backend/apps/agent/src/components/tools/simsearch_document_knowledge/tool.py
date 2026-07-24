import os
import requests
from pydantic import BaseModel, Field
from langchain.tools import tool, ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from src.core.context_model import ContextAgent
from dotenv import load_dotenv

load_dotenv()

class SimSearchDocumentInput(BaseModel):
    query: str = Field(description="Tentukan query yang sesuai")

@tool(args_schema=SimSearchDocumentInput)
def similarity_search_document_knowledge(query: str, runtime: ToolRuntime[ContextAgent]):
    """Untuk mengambil informasi dari dokument knowledge yang tersedia"""
    backend_url = os.environ.get("BACKEND_URL")
    configurable = runtime.context or {}
    agent_id = configurable.get("agent_id")

    response = requests.post(f"{backend_url}/api/document_knowladge/similarity_search" or "http://localhost:8000/api/document_knowladge/similarity_search", json={"agent_id": agent_id, "query": query})
    if response.status_code != 200:
        return "Terjadi kesalahan sistem saat mendapatkan dokument knowledge"
    
    result = response.json()
    return Command(
        update={
            "messages": [ToolMessage(content=result["data"]["result"], tool_call_id=runtime.tool_call_id)],
        }
    )