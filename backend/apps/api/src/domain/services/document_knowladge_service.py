from uuid import UUID

from fastapi import UploadFile
from src.app.validators.document_knowladge_schema import AddDocumentKnowladge
from src.core.context.request_context import current_user_id, current_user_email
from src.core.exceptions.agent_exception import AgentNotFound
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.utils.save_file import save_file_handler
from src.domain.repositories import AgentRepository, DocumentKnowladgeRepository
from src.domain.usecases.agent import (
    DeleteDocumentKnowladgeUsecase,
    DeleteDocumentKnowladgeUsecaseInput,
    FileUploadUseCase,
    FileUploadUseCaseInput,
    GetAllDocumentKnowladgeUsecase,
    GetAllDocumentKnowladgeUsecaseInput,
    RagProcessUseCase,
    RagProcessUsecaseInput,
)
from src.infrastructure.vectorstore.chroma_db import rag_system
from supabase import AsyncClient

from .base import BaseService


class DocumentKnowladgeService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        # repositories
        self.agent_repo = AgentRepository(self.db)
        self.document_knowladge_repo = DocumentKnowladgeRepository(self.db)

        # dependecies
        self.rag_system = rag_system
        self.save_file_handler = save_file_handler

        # usecases
        self.file_upload_usecase = FileUploadUseCase(self.save_file_handler)
        self.rag_process_usecase = RagProcessUseCase(
            self.document_knowladge_repo, self.rag_system
        )
        self.get_all_document_knowladge_usecase = GetAllDocumentKnowladgeUsecase(
            self.document_knowladge_repo, self.rag_system
        )
        self.delete_document_knowladge_usecase = DeleteDocumentKnowladgeUsecase(
            self.document_knowladge_repo, self.save_file_handler, self.rag_system
        )

        super().__init__(__name__)

    async def get_all_document_knowladges(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get all document knowladges")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        usecase_result = await self.get_all_document_knowladge_usecase.execute(
            GetAllDocumentKnowladgeUsecaseInput(agent_id=agent_id)
        )
        if not usecase_result.is_success():
            self.logger.error(
                f"User {user_email}: Get all document knowladge usecase is error"
            )
            self.raise_error_usecase(usecase_result)

        result_data = usecase_result.get_data()
        if result_data is None:
            raise RuntimeError(
                "get all document knowladges usecase did not returned the data"
            )
        self.logger.info(
            f"User {user_email}: get all document knowladge is successfully"
        )
        return result_data.document_knowladge_list

    async def add_document_to_agent(self, file: UploadFile, file_description: str):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: add document to agent")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: agent not found")
            raise AgentNotFound()

        file_upload_result = await self.file_upload_usecase.execute(
            FileUploadUseCaseInput(user_id, agent_id, file)
        )

        if not file_upload_result.is_success():
            self.logger.error(f"User {user_email}: File upload usecase is error")
            self.raise_error_usecase(file_upload_result)

        file_data = file_upload_result.get_data()
        if file_data is None:
            raise RuntimeError("file upload usecase did not returned the data")

        document_data = AddDocumentKnowladge(
            title=file.filename,
            description=file_description,
            file_path=file_data.directory_path,
            file_format=file_data.content_type,
            file_size=file_data.file_size,
        )
        rag_result = await self.rag_process_usecase.execute(
            RagProcessUsecaseInput(agent_id, document_data)
        )
        if not rag_result.is_success():
            self.logger.error(f"User {user_email}: Rag processs usecase is error")
            self.raise_error_usecase(rag_result)
        rag_result_data = rag_result.get_data()
        if rag_result_data is None:
            raise RuntimeError("file rag process usecase did not returned the data")
        self.logger.info(f"User {user_email}: add document to agent is successfully")

        return rag_result_data.document_data

    async def delete_document_knowladge(self, document_knowladge_id: UUID):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: delete document knowladge")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")

            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: agent not found")
            raise AgentNotFound()

        usecase_result = await self.delete_document_knowladge_usecase.execute(
            DeleteDocumentKnowladgeUsecaseInput(document_knowladge_id, agent_id)
        )

        if not usecase_result.is_success():
            self.logger.error(
                f"User {user_email}: Delete document knowladge usecase is error"
            )
            self.raise_error_usecase(usecase_result)

        result_data = usecase_result.get_data()
        if result_data is None:
            raise RuntimeError(
                "delete document knowladge usecase did not returned the data"
            )
        self.logger.info(
            f"User {user_email}: delete document knowladge is successfully"
        )

        return result_data.document_knowladge_data
