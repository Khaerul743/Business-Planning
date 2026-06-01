from uuid import UUID
from supabase import AsyncClient
from shared.schemas.business_knowladge import BusinessKnowladge
from shared.utils.logger import get_logger
from shared.schemas import Business, DocumentKnowladge, BusinessKnowladge
from shared.schemas import AgentConfiguration


class KnowladgeRepository:
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def get_business_by_id(self, business_id: UUID) -> Business | None:
        try:
            result = (
                await self.db.table("Businesses")
                .select("*")
                .eq("id", business_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
            return Business.model_validate(result.data)
        except Exception as e:
            self._logger.error(f"Error while get business by id: {str(e)}")

    async def get_all_business_knowladge_by_business_id(
        self, business_id: UUID
    ) -> list[BusinessKnowladge] | None:
        try:
            result = (
                await self.db.table("Business_knowladges")
                .select("*")
                .eq("business_id", str(business_id))
                .execute()
            )
            print(result)
            if result is None:
                return None
            data = result.data

            list_data = []
            for i in data:
                list_data.append(BusinessKnowladge.model_validate(i))

            return list_data
        except Exception as e:
            raise e

    async def get_all_document_knowladge_by_agent_id(
        self, agent_id: UUID
    ) -> list[DocumentKnowladge] | None:
        try:

            result = (
                await self.db.table("Document_knowladges")
                .select("*")
                .eq("agent_id", agent_id)
                .execute()
            )
            if len(result.data) == 0:
                return None

            document_knowladge_list = []
            for i in result.data:
                document_knowladge_list.append(DocumentKnowladge.model_validate(i))

            return document_knowladge_list
        except Exception as e:
            self._logger.error(
                f"Error while get all document knowladge by agent id: {str(e)}"
            )
            raise e

    async def get_agent_conf_by_agent_id(
        self, agent_id: UUID
    ) -> AgentConfiguration | None:
        result = (
            await self.db.table("Agent_configurations")
            .select("*")
            .eq("agent_id", agent_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            return None

        return AgentConfiguration.model_validate(result.data)
