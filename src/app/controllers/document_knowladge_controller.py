from fastapi import UploadFile
from supabase import AsyncClient

from src.domain.services import DocumentKnowladgeService

from .base import BaseController


class DocumentKnowladgeController(BaseController):
    def __init__(self, db: AsyncClient):
        self.document_knowladge_service = DocumentKnowladgeService(db)

    async def get_all_document_knowladges_handler(self):
        try:
            result = await self.document_knowladge_service.get_all_document_knowladges()
            return result
        except Exception as e:
            raise e

    async def add_document_to_agent_handler(
        self, file: UploadFile, file_description: str
    ):
        try:
            result = await self.document_knowladge_service.add_document_to_agent(
                file, file_description
            )
            return result.model_dump()

        except Exception as e:
            raise e

    async def delete_document_knowladge_handler(self, document_knowladge_id: int):
        try:
            result = await self.document_knowladge_service.delete_document_knowladge(
                document_knowladge_id
            )
            return result.model_dump()
        except Exception as e:
            raise e
