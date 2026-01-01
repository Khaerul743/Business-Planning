from typing import Literal, Optional

from pydantic import BaseModel


# Create agent
class CreateAgentIn(BaseModel):
    name: str
    llm_provider: str
    llm_model: str
    temperature: Optional[float] = 0.7
    enable_ai: Optional[bool] = True
    fallback_to_human: str


# Agent configuration
class WhatsappAgentConfig(BaseModel):
    chromadb_path: str
    collection_name: str
    llm_provider: str
    llm_model: str
    tone: Literal["friendly", "formal", "casual", "profesional"]
    base_prompt: str
    include_memory: bool = False
    user_memory_id: Optional[str] = None
