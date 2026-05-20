from src.app.validators.agent_schema import AgentConf
from src.infrastructure.ai.agent.wa_agent import WhatsappAgent
from src.infrastructure.ai.agent.wa_agent.schema import (
    BusinessDetailInformation,
    BusinessKnowladgeContent,
    DocumentRagDetail,
)

# business_inf = BusinessDetailInformation(
#     business_name="Rusdi store",
#     business_desc="Merupakan salah satu online store paling laris di ngawi selatan",
#     business_location="Ngawi selatan, kec. Rongawi, kab. Rongawi Kuno",
# )

# bk = {
#     "owner": {"description": "untuk mengetahui nama owner", "content": "rusdi"},
#     "product": {
#         "description": "product yang tersedia di rusdi barber",
#         "content": "- Gatsby pomade by amba\n- shampo muani maknyus\n- Minyak rambut khas bumi ayu",
#     },
# }


class WhatsappAgentManager:
    def __init__(self):
        self._agents: dict[int | str, WhatsappAgent] = {}

    def get_or_create_by_business_id(
        self,
        business_id: int,
        config: AgentConf,
        business_detail_information: BusinessDetailInformation,
        business_knowladge: dict[str, BusinessKnowladgeContent],
        document_rag_detail: list[DocumentRagDetail],
    ) -> WhatsappAgent:
        if business_id not in self._agents:
            self._agents[business_id] = WhatsappAgent(
                chromadb_path=config.chromadb_path,
                collection_name=config.collection_name,
                llm_provider=config.llm_provider,
                llm_model=config.llm_model,
                tone=config.tone,
                base_prompt=config.base_prompt,
                business_detail_information=business_detail_information,
                business_knowladge=business_knowladge,
                document_rag_detail=document_rag_detail,
            )
        return self._agents[business_id]

    def get_or_create_by_phone_number_id(
        self,
        phone_number_id: str,
        config: AgentConf,
        business_detail_information: BusinessDetailInformation,
        business_knowladge: dict[str, BusinessKnowladgeContent],
        document_rag_detail: list[DocumentRagDetail],
    ) -> WhatsappAgent:
        if phone_number_id not in self._agents:
            self._agents[phone_number_id] = WhatsappAgent(
                chromadb_path=config.chromadb_path,
                collection_name=config.collection_name,
                llm_provider=config.llm_provider,
                llm_model=config.llm_model,
                tone=config.tone,
                base_prompt=config.base_prompt,
                business_detail_information=business_detail_information,
                business_knowladge=business_knowladge,
                document_rag_detail=document_rag_detail,
            )
        return self._agents[phone_number_id]

    def get_agent_by_phone_number_id(self, phone_number_id: str):
        return self._agents[phone_number_id]

    def remove(self, business_id: int):
        self._agents.pop(business_id, None)

    def exists(self, phone_number_id: str) -> bool:
        return phone_number_id in self._agents

    def remove_agent_by_phone_number_id(self, phone_number_id: str):
        self._agents.pop(phone_number_id, None)


whatsapp_agent_manager = WhatsappAgentManager()
