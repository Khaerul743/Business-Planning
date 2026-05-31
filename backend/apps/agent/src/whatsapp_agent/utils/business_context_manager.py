from uuid import UUID
from supabase import AsyncClient
from src.repositories.knowladge_repository import KnowladgeRepository
from src.whatsapp_agent.schema.business_context import (
    BusinessDetailInformation,
    BusinessKnowladgeContent,
    DocumentRagDetail,
    BusinessContext,
)
from shared.utils.logger import get_logger


class BusinessContextManager:
    def __init__(self, db: AsyncClient):
        self.cache: dict[str, BusinessContext] = {}
        self.business_knowladge_repo = KnowladgeRepository(db)
        self._logger = get_logger(__name__)

    async def _get_business_information(
        self, business_id: UUID
    ) -> BusinessDetailInformation | None:
        business = await self.business_knowladge_repo.get_business_by_id(business_id)
        if business is None:
            self._logger.warning("Business not found")
            return
        business_detail_information = BusinessDetailInformation(
            business_name=business.name,
            business_desc=business.description,
            business_location=business.address,
        )
        return business_detail_information

    async def _get_business_knowladge(
        self, business_id: UUID
    ) -> dict[str, BusinessKnowladgeContent] | None:
        business_knowladge = await self.business_knowladge_repo.get_all_business_knowladge_by_business_id(
            business_id
        )
        if business_knowladge is None:
            self._logger.warning("Business knowladge not found")
            return
        list_business_knowladge: dict[str, BusinessKnowladgeContent] = {}
        for value in business_knowladge:
            list_business_knowladge[value.category] = BusinessKnowladgeContent(
                category_description=value.category_description,
                content=value.content,
            )
        return list_business_knowladge

    async def _get_document_knowladge(
        self, agent_id: UUID
    ) -> list[DocumentRagDetail] | None:
        document_knowladge = (
            await self.business_knowladge_repo.get_all_document_knowladge_by_agent_id(
                agent_id
            )
        )
        if document_knowladge is None:
            self._logger.warning("Document knowladge not found")
            return
        list_document_knowladge = [
            DocumentRagDetail(title=i.title, description=i.description)
            for i in document_knowladge
        ]
        return list_document_knowladge

    async def get_context(self, agent_id: UUID, business_id: UUID) -> BusinessContext:
        business_context = self.cache.get(str(business_id), None)
        if business_context is None:
            business_information = await self._get_business_information(business_id)
            business_knowladge = await self._get_business_knowladge(business_id)
            document_knowladge = await self._get_document_knowladge(agent_id)
            business_context = BusinessContext(
                business_detail_information=business_information,
                business_knowladge_content=business_knowladge,
                document_rag_detail=document_knowladge,
            )
            self.cache[str(business_id)] = business_context

        return business_context
