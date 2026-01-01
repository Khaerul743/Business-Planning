from supabase import AsyncClient

from src.app.validators.agent_schema import CreateAgentIn
from src.core.context.request_context import current_user_id
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.repositories import AgentRepository, BusinessRepository
from src.domain.usecases.agent import CreateAgentUseCase, CreateAgentUseCaseInput
from src.infrastructure.ai.agent.manager import whatsapp_agent_manager

from .base import BaseService


class AgentService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        # repositories
        self.agent_repo = AgentRepository(self.db)
        self.business_repo = BusinessRepository(self.db)

        # dependencies
        self.whatsapp_agent_manager = whatsapp_agent_manager

        # Use case
        self.create_agent_usecase = CreateAgentUseCase(
            self.agent_repo, self.whatsapp_agent_manager
        )

        super().__init__(__name__)

    async def create_new_agent(self, payload: CreateAgentIn):
        try:
            user_id = current_user_id.get()
            if user_id is None:
                raise UnauthorizedException()

            business_id = await self.business_repo.get_business_id_by_user_id(user_id)
            if business_id is None:
                raise BusinessNotFound()

            result = await self.create_agent_usecase.execute(
                CreateAgentUseCaseInput(business_id=business_id, agent_data=payload)
            )
            if not result.is_success():
                self.raise_error_usecase(result)

            result_data = result.get_data()
            if result_data is None:
                raise RuntimeError("Create agent usecase did not returned the data")

            return result_data.agent_data

        except UnauthorizedException as e:
            self.logger.warning(str(e))
            raise e

        except BusinessNotFound as e:
            self.logger.warning(str(e))
            raise e

        except RuntimeError as e:
            self.logger.error(str(e))
            raise e
