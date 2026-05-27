from dataclasses import dataclass
from uuid import UUID

from src.app.validators.agent_schema import AgentConf
from src.core.exceptions.agent_exception import (
    AgentConfigurationNotFound,
    DocumentKnowladgeNotFound,
)
from src.core.exceptions.business_exception import BusinessNotFound
from src.core.exceptions.business_knowladge_exception import BusinessKnowladgeNotFound
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import (
    IAgentConfigurationRepository,
    IBusinessKnowladgeRepository,
    IBusinessRepository,
    IDocumentKnowladgeRepository,
)
from src.infrastructure.ai.agent.manager import WhatsappAgentManager
from src.infrastructure.ai.agent.wa_agent import WhatsappAgent
from src.infrastructure.ai.agent.wa_agent.schema import (
    BusinessDetailInformation,
    BusinessKnowladgeContent,
    DocumentRagDetail,
)


@dataclass
class CreateAgentObjInput:
    business_id: UUID
    phone_number_id: str
    agent_id: UUID


@dataclass
class CreateAgentObjOutput:
    agent: WhatsappAgent


class CreateAgentObjUseCase(BaseUseCase[CreateAgentObjInput, CreateAgentObjOutput]):
    def __init__(
        self,
        agent_conf_repo: IAgentConfigurationRepository,
        business_repo: IBusinessRepository,
        document_knowladge_repo: IDocumentKnowladgeRepository,
        business_knowladge_repo: IBusinessKnowladgeRepository,
        wa_agent_manager: WhatsappAgentManager,
    ):
        self.agent_conf_repo = agent_conf_repo
        self.business_repo = business_repo
        self.document_knowladge_repo = document_knowladge_repo
        self.business_knowladge_repo = business_knowladge_repo
        self.wa_agent_manager = wa_agent_manager

    async def execute(
        self, input_data: CreateAgentObjInput
    ) -> UseCaseResult[CreateAgentObjOutput]:
        try:
            # Define business detail information
            business = await self.business_repo.get_business_by_id(
                input_data.business_id
            )
            if business is None:
                return UseCaseResult.error_result(
                    "Business not found", BusinessNotFound()
                )

            business_detail_information = BusinessDetailInformation(
                business_name=business.name,
                business_desc=business.description,
                business_location=business.address,
            )
            # Define business knowladge content
            business_knowladge = await self.business_knowladge_repo.get_all_business_knowladge_by_business_id(
                input_data.business_id
            )
            if business_knowladge is None:
                return UseCaseResult.error_result(
                    "Business knowladge not found", BusinessKnowladgeNotFound()
                )

            list_business_knowladge: dict[str, BusinessKnowladgeContent] = {}
            for value in business_knowladge:
                list_business_knowladge[value.category] = BusinessKnowladgeContent(
                    category_description=value.category_description,
                    content=value.content,
                )

            # Define document rag detail
            document_knowladge = await self.document_knowladge_repo.get_all_document_knowladge_by_agent_id(
                input_data.agent_id
            )
            if document_knowladge:
                list_document_knowladge_detail = [
                    DocumentRagDetail(title=i.title, description=i.description)
                    for i in document_knowladge
                ]
            else:
                list_document_knowladge_detail = None

            # Get agent configuration
            agent_conf = await self.agent_conf_repo.get_agent_conf_by_agent_id(
                input_data.agent_id
            )
            if agent_conf is None:
                return UseCaseResult.error_result(
                    "Agent configuration not found", AgentConfigurationNotFound()
                )

            agent_config = AgentConf(
                chromadb_path=agent_conf.chromadb_path,
                collection_name=agent_conf.collection_name,
                llm_model=agent_conf.llm_model,
                llm_provider=agent_conf.llm_provider,
                tone=agent_conf.tone,
                base_prompt=agent_conf.base_prompt,
                temperature=agent_conf.temperature,
            )

            agent = self.wa_agent_manager.get_or_create_by_phone_number_id(
                input_data.phone_number_id,
                agent_config,
                business_detail_information,
                list_business_knowladge,
                list_document_knowladge_detail,
            )

            return UseCaseResult.success_result(CreateAgentObjOutput(agent))
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while creating agent obj: {e}", e
            )
