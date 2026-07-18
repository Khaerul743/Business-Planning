from uuid import UUID
from dataclasses import dataclass
from langgraph_sdk import get_client
from src.config import settings

@dataclass
class CustomerServiceAgentConfig:
    business_id: str
    agent_id: str

class AgentManager:
    def __init__(self):
        self.client = get_client(url=settings.LANGGRAPH_SERVER)
    
    async def run_customer_service_agent(self, thread_id: str, config: CustomerServiceAgentConfig, user_message: str):
        agent_config = {
            "configurable":{
                "business_id": config.business_id,
                "agent_id": config.agent_id
            }
        }

        inputs = {"messages": [], "user_message": user_message}
        return await self.client.runs.wait(
            thread_id=thread_id,
            assistant_id="customer_service_agent",
            config=agent_config,
            input=inputs
        )

    async def register_thread_id(self, thread_id: UUID):
        thread_id_str = str(thread_id)
        thread = await self.client.threads.create(thread_id=thread_id_str)
        return thread["thread_id"]
    

langgraph_client = AgentManager()
