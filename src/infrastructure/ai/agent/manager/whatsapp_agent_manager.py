from src.app.validators.agent_schema import AgentConf
from src.infrastructure.ai.agent.whatsapp_agent import WhatsappAgent


class WhatsappAgentManager:
    def __init__(self):
        self._agents: dict[int | str, WhatsappAgent] = {}

    def get_or_create_by_business_id(
        self, business_id: int, config: AgentConf
    ) -> WhatsappAgent:
        if business_id not in self._agents:
            self._agents[business_id] = WhatsappAgent(
                chromadb_path=config.chromadb_path,
                collection_name=config.collection_name,
                llm_provider=config.llm_provider,
                llm_model=config.llm_model,
                tone=config.tone,
                base_prompt=config.base_prompt,
                include_long_memory=config.include_memory,
                user_memory_id=config.user_memory_id,
            )
        return self._agents[business_id]

    def get_or_create_by_phone_number_id(
        self, phone_number_id: str, config: AgentConf
    ) -> WhatsappAgent:
        if phone_number_id not in self._agents:
            self._agents[phone_number_id] = WhatsappAgent(
                chromadb_path=config.chromadb_path,
                collection_name=config.collection_name,
                llm_provider=config.llm_provider,
                llm_model=config.llm_model,
                tone=config.tone,
                base_prompt=config.base_prompt,
                include_long_memory=config.include_memory,
                user_memory_id=config.user_memory_id,
            )
        return self._agents[phone_number_id]

    def remove(self, business_id: int):
        self._agents.pop(business_id, None)

    def exists(self, business_id: int) -> bool:
        return business_id in self._agents


whatsapp_agent_manager = WhatsappAgentManager()
