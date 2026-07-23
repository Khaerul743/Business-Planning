from dataclasses import dataclass

from src.infrastructure.vectorstore.chroma_db import RAGSystem
from src.config import settings
from src.domain.usecases.base import UseCaseResult, BaseUseCase

@dataclass
class GetRagSimSearchInput:
    agent_id: str
    query: str

@dataclass
class GetRagSimSearchOutput:
    result: str


class GetRagSimSearch(BaseUseCase[GetRagSimSearchInput, GetRagSimSearchOutput]):
    def __init__(self):
        self.rag_system = RAGSystem(chroma_directiory=settings.CHROMADB_PATH)
        super().__init__(__name__)

    async def execute(self, input_data: GetRagSimSearchInput) -> UseCaseResult[GetRagSimSearchOutput]:
        try:
            self.rag_system.initial_collection(f"agent_{str(input_data.agent_id)}")
            result = self.rag_system.similarity_search(input_data.query)
            return UseCaseResult.success_result(GetRagSimSearchOutput(result=result))
        except Exception as e:
            self.logger.error(f"Error while get sim search: {e}")
            return UseCaseResult.error_result(f"Error while get sim search: {e}",e)

    