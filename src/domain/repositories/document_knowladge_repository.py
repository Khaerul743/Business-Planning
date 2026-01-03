from supabase import AsyncClient

from src.app.validators.document_knowladge_schema import AddDocumentKnowladge
from src.domain.models import Document_knowladge
from src.domain.usecases.interfaces import IDocumentKnowladgeRepository


class DocumentKnowladgeRepository(IDocumentKnowladgeRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def delete_document_knowladge_by_id_n_agent_id(
        self, document_knowladge_id: int, agent_id: int
    ) -> Document_knowladge | None:
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

    async def get_all_document_knowladge_by_agent_id(
        self, agent_id: int
    ) -> list[Document_knowladge] | None:
        result = (
            await self.db.table("Document_knowladges")
            .select("*")
            .eq("agent_id", agent_id)
            .execute()
        )
        if result is None:
            return None

        document_knowladge_list = []
        for i in result.data:
            document_knowladge_list.append(Document_knowladge.model_validate(i))

        return document_knowladge_list

    async def insert_document_knowladge(
        self, agent_id: int, document_data: AddDocumentKnowladge
    ) -> Document_knowladge:
        payload = document_data.model_dump()
        payload["agent_id"] = agent_id
        result = await self.db.table("Document_knowladges").insert(payload).execute()

        return Document_knowladge.model_validate(result.data[0])
