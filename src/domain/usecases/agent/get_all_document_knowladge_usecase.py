from dataclasses import dataclass

from src.core.exceptions.agent_exception import DocumentKnowladgeNotFound
from src.domain.models import Document_knowladge
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IDocumentKnowladgeRepository
from src.infrastructure.vectorstore.chroma_db import RAGSystem


@dataclass
class GetAllDocumentKnowladgeUsecaseInput:
    agent_id: int


@dataclass
class GetAllDocumentKnowladgeUsecaseOutput:
    document_knowladge_list: list[Document_knowladge]


class GetAllDocumentKnowladgeUsecase(
    BaseUseCase[
        GetAllDocumentKnowladgeUsecaseInput, GetAllDocumentKnowladgeUsecaseOutput
    ]
):
    def __init__(
        self,
        document_knowladge_repo: IDocumentKnowladgeRepository,
        rag_system: RAGSystem,
    ):
        self.document_knowladge_repo = document_knowladge_repo
        self.rag_system = rag_system

    async def execute(
        self, input_data: GetAllDocumentKnowladgeUsecaseInput
    ) -> UseCaseResult[GetAllDocumentKnowladgeUsecaseOutput]:
        try:
            # initial collection
            self.rag_system.initial_collection(f"agent_{input_data.agent_id}")

            list_document_knowladge = await self.document_knowladge_repo.get_all_document_knowladge_by_agent_id(
                input_data.agent_id
            )

            if list_document_knowladge is None:
                return UseCaseResult.error_result(
                    "Document knowladge is not found", DocumentKnowladgeNotFound()
                )

            list_document_vector = self.rag_system.list_documents()

            list_document_result: list[Document_knowladge] = []

            for i in list_document_knowladge:
                if i.id in list_document_vector:
                    list_document_result.append(i)

            if len(list_document_result) == 0:
                return UseCaseResult.error_result(
                    "Document knowladge is not found", DocumentKnowladgeNotFound()
                )

            return UseCaseResult.success_result(
                GetAllDocumentKnowladgeUsecaseOutput(list_document_result)
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting all document knowladge: {str(e)}", e
            )
