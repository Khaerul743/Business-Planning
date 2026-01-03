from dataclasses import dataclass

from src.app.validators.document_knowladge_schema import AddDocumentKnowladge
from src.domain.models import Document_knowladge
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IDocumentKnowladgeRepository
from src.infrastructure.vectorstore.chroma_db import RAGSystem


@dataclass
class RagProcessUsecaseInput:
    agent_id: int
    document_data: AddDocumentKnowladge


@dataclass
class RagProcessUsecaseOutput:
    document_data: Document_knowladge
    chunk_ids: list[str]


class RagProcessUseCase(BaseUseCase[RagProcessUsecaseInput, RagProcessUsecaseOutput]):
    def __init__(
        self,
        document_knowladge_repo: IDocumentKnowladgeRepository,
        rag_system: RAGSystem,
    ):
        self.rag_system = rag_system
        self.document_knowladge_repo = document_knowladge_repo

    async def execute(
        self, input_data: RagProcessUsecaseInput
    ) -> UseCaseResult[RagProcessUsecaseOutput]:
        try:
            # Add document knowladge entity
            response = await self.document_knowladge_repo.insert_document_knowladge(
                input_data.agent_id, input_data.document_data
            )

            # Initial collection name
            self.rag_system.initial_collection(f"agent_{input_data.agent_id}")

            # Document process chunking
            list_document = self.rag_system.load_single_document(
                input_data.document_data.file_path,
                input_data.document_data.title,
                input_data.document_data.file_format,
            )

            # Add document to vectorstore
            chunk_ids = self.rag_system.add_documents(list_document, response.id)

            return UseCaseResult.success_result(
                RagProcessUsecaseOutput(document_data=response, chunk_ids=chunk_ids)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while rag process: {str(e)}", e
            )
