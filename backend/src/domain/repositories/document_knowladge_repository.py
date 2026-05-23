from uuid import UUID

from supabase import AsyncClient

from src.app.validators.document_knowladge_schema import AddDocumentKnowladge
from src.domain.models import Document_knowladge
from src.domain.usecases.interfaces import IDocumentKnowladgeRepository
from src.core.utils.logger import get_logger


class DocumentKnowladgeRepository(IDocumentKnowladgeRepository):
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def delete_document_knowladge_by_id_n_agent_id(
        self, document_knowladge_id: UUID, agent_id: UUID
    ) -> Document_knowladge | None:
        try:
            result = (
                await self.db.table("Document_knowladges")
                .delete()
                .eq("agent_id", agent_id)
                .eq("id", document_knowladge_id)
                .execute()
            )
            if len(result.data) == 0:
                return None

            return Document_knowladge.model_validate(result.data[0])
        except Exception as e:
            self._logger.error(
                f"Error while delete document knowladge by id n adgent id: {str(e)}"
            )
            raise e

    async def get_all_document_knowladge_by_agent_id(
        self, agent_id: UUID
    ) -> list[Document_knowladge] | None:
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
                document_knowladge_list.append(Document_knowladge.model_validate(i))

            return document_knowladge_list
        except Exception as e:
            self._logger.error(
                f"Error while get all document knowladge by agent id: {str(e)}"
            )
            raise e

    async def insert_document_knowladge(
        self, agent_id: UUID, document_data: AddDocumentKnowladge
    ) -> Document_knowladge:
        try:

            payload = document_data.model_dump()
            payload["agent_id"] = str(agent_id)
            result = (
                await self.db.table("Document_knowladges").insert(payload).execute()
            )

            return Document_knowladge.model_validate(result.data[0])
        except Exception as e:
            self._logger.error(f"Error while insert document knowladge: {str(e)}")
            raise e
