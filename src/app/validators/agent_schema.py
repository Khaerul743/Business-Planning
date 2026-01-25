from typing import Literal, Optional

from pydantic import BaseModel


# Insert New Agent
class InsertAgent(BaseModel):
    phone_number_id: Optional[str] = None
    name: str
    enable_ai: Optional[bool] = True
    fallback_to_human: str


# Create agent
class CreateAgentIn(BaseModel):
    name: str
    llm_provider: str
    llm_model: str
    base_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    enable_ai: Optional[bool] = True
    tone: Literal["friendly", "formal", "casual", "profesional"]
    include_memory: bool = False
    fallback_to_human: str


# Agent configuration
class AgentConf(BaseModel):
    chromadb_path: Optional[str] = None
    collection_name: Optional[str] = None
    llm_provider: str
    llm_model: str
    tone: Literal["friendly", "formal", "casual", "profesional"]
    base_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    include_memory: bool = False
    user_memory_id: Optional[str] = None
