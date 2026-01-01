from typing import Literal, Optional

from langgraph.checkpoint.memory import MemorySaver

# from langgraph.checkpoint.redis import RedisSaver
# from src.infrastructure.redis.redis_storage import RedisStorage
from src.infrastructure.ai.agent.base import BaseAgent
from src.infrastructure.ai.agent.components.tools import RetrieveDocumentTool

from .nodes import SimpleRagAgentNodes
from .prompts import SimpleRagPrompt
from .workflow import SimpleRagWorkflow


class WhatsappAgent(BaseAgent):
    def __init__(
        self,
        chromadb_path: str,
        collection_name: str,
        llm_provider: str,
        llm_model: str,
        tone: Literal["friendly", "formal", "casual", "profesional"],
        base_prompt: Optional[str] = None,
        include_long_memory: bool = False,
        user_memory_id: Optional[str] = None,
    ):
        self.retrieve_document_tool = RetrieveDocumentTool(
            chromadb_path, collection_name
        )
        # self.state_saver = RedisStorage()
        # self.checkpoint = RedisSaver(redis_url=self.state_saver.redis_url)
        self.checkpoint = MemorySaver()
        self.prompts = SimpleRagPrompt(tone, base_prompt)
        self.agent_node = SimpleRagAgentNodes(
            self.prompts,
            self.retrieve_document_tool,
            llm_model,
            llm_provider,
            include_long_memory,
            user_memory_id,
        )
        self.agent_workflow = SimpleRagWorkflow(self.agent_node, self.checkpoint)
        super().__init__(self.agent_node, self.agent_workflow)
