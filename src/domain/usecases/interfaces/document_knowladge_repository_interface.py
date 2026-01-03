from abc import ABC, abstractmethod

from src.app.validators.document_knowladge_schema import AddDocumentKnowladge
from src.domain.models import Document_knowladge


class IDocumentKnowladgeRepository(ABC):
    @abstractmethod
    async def delete_document_knowladge_by_id_n_agent_id(
        self, document_knowladge_id: int, agent_id: int
    ) -> Document_knowladge | None:
        pass

    @abstractmethod
    async def get_all_document_knowladge_by_agent_id(
        self, agent_id: int
    ) -> list[Document_knowladge] | None:
        pass

    @abstractmethod
    async def insert_document_knowladge(
        self, agent_id: int, document_data: AddDocumentKnowladge
    ) -> Document_knowladge:
        pass
