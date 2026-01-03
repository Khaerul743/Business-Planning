from dataclasses import dataclass

from src.core.exceptions.agent_exception import DocumentKnowladgeNotFound
from src.core.utils.save_file import SaveFileHandler
from src.domain.models import Document_knowladge
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IDocumentKnowladgeRepository
from src.infrastructure.vectorstore.chroma_db import RAGSystem


@dataclass
class DeleteDocumentKnowladgeUsecaseInput:
    document_knowladge_id: int
    agent_id: int


@dataclass
class DeleteDocumentKnowladgeUsecaseOutput:
    document_knowladge_data: Document_knowladge


class DeleteDocumentKnowladgeUsecase(
    BaseUseCase[
        DeleteDocumentKnowladgeUsecaseInput, DeleteDocumentKnowladgeUsecaseOutput
    ]
):
    def __init__(
        self,
        document_knowladge_repo: IDocumentKnowladgeRepository,
        save_file_handler: SaveFileHandler,
        rag_system: RAGSystem,
    ):
        self.document_knowladge_repo = document_knowladge_repo
        self.save_file_handler = save_file_handler
        self.rag_system = rag_system

    async def execute(
        self, input_data: DeleteDocumentKnowladgeUsecaseInput
    ) -> UseCaseResult[DeleteDocumentKnowladgeUsecaseOutput]:
        try:
            document_knowladge = await (
                self.document_knowladge_repo.delete_document_knowladge_by_id_n_agent_id(
                    input_data.document_knowladge_id, input_data.agent_id
                )
            )

            if document_knowladge is None:
                return UseCaseResult.error_result(
                    "Document not found", DocumentKnowladgeNotFound()
                )

            self.save_file_handler.delete_file(
                document_knowladge.file_path, document_knowladge.title
            )

            # delete vector
            self.rag_system.delete_document(document_knowladge.id)

            return UseCaseResult.success_result(
                DeleteDocumentKnowladgeUsecaseOutput(document_knowladge)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while deleting document knowladge usecase: {str(e)}",
                e,
            )
