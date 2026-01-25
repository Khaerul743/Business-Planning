from typing import Literal, Optional

from .base import BaseEntity


class Agent_configuration(BaseEntity):
    agent_id: int
    chromadb_path: Optional[str] = None
    collection_name: Optional[str] = None
    llm_provider: str
    llm_model: str
    base_prompt: Optional[str] = None
    tone: Literal["friendly", "casual", "profesional", "formal"]
    temperature: Optional[float] = 0.7
    include_memory: bool = False
    user_memory_id: Optional[str] = None
