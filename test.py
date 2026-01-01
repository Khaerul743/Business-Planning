from src.app.validators.agent_schema import WhatsappAgentConfig
from src.infrastructure.ai.agent.manager import WhatsappAgentManager

manager = WhatsappAgentManager()

agent_conf = WhatsappAgentConfig(
    chromadb_path="chromadb",
    collection_name="my_collection",
    llm_provider="openai",
    llm_model="gpt-3.5-turbo",
    tone="casual",
    base_prompt="",
)

agent = manager.get_or_create(1, agent_conf)

print(agent.get_llm_model())
