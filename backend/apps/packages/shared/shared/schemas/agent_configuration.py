from typing import Literal, Optional
from uuid import UUID

from .base import BaseEntity, BaseModel


class AgentConfiguration(BaseEntity):
    agent_id: UUID
    chromadb_path: Optional[str] = None
    collection_name: Optional[str] = None
    llm_provider: str
    llm_model: str
    base_prompt: Optional[str] = None
    fallback_email: str
    tone: Literal["friendly", "casual", "profesional", "formal"]
    temperature: Optional[float] = 0.7


# Agent configuration
class AgentConfig(BaseModel):
    chromadb_path: Optional[str] = None
    collection_name: Optional[str] = None
    llm_provider: Literal["openai", "google", "anthropic"]
    llm_model: str
    tone: Literal["friendly", "formal", "casual", "profesional"]
    base_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
