from uuid import uuid4
from supabase import AsyncClient

from src.app.validators.agent_schema import CreateAgentIn, UpdateAgentIn
from src.core.context.request_context import current_user_id, current_user_email
from src.core.exceptions.agent_exception import AgentNotFound, InsightNotFound
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import BusinessNotFound
from src.domain.repositories import (
    AgentConfigurationRepository,
    AgentRepository,
    AnalyticsRepository,
    BusinessKnowladgeRepository,
    BusinessRepository,
    DocumentKnowladgeRepository,
    InsightRepository,
)
from src.domain.usecases.agent import (
    CreateAgentObjUseCase,
    CreateAgentUseCase,
    CreateAgentUseCaseInput,
    GetAgentInput,
    GetAgentUseCase,
    InvokeAgentInput,
    InvokeAgentUseCase,
    UpdateAgentInput,
    UpdateAgentUseCase,
)
from src.domain.usecases.analytic import (
    GetAgentAnalyticsInput,
    GetAgentAnalyticsUseCase,
    GetCategoryPercentages,
    GetCategoryPercentagesInput,
    GetHumanVsAiMessageTrendInput,
    GetHumanVsAiMessageTrendUseCase,
    GetMessageUsageTrendInput,
    GetMessageUsageTrendUseCase,
    GetTokenUsageTrendInput,
    GetTokenUsageTrendUseCase,
)
from src.domain.usecases.insight import (
    GenerateInsight,
    GenerateGapKnowladgeInput,
    GenerateGapKnowladge,
)
from src.infrastructure.ai.agent.manager import whatsapp_agent_manager
from src.infrastructure.ai.agent.wa_agent import WhatsappAgentState

from .base import BaseService
from src.infrastructure.queue.redis import redis_client
from src.infrastructure.queue import RedisQueue


class AgentService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        # Queue
        self.redis_queue = RedisQueue(redis_client, "generator_queue")

        # repositories
        self.agent_repo = AgentRepository(self.db)
        self.agent_conf_repo = AgentConfigurationRepository(db)
        self.business_repo = BusinessRepository(self.db)
        self.analytic_repo = AnalyticsRepository(self.db)
        self.document_knowladge_repo = DocumentKnowladgeRepository(self.db)
        self.business_knowladge_repo = BusinessKnowladgeRepository(self.db)
        self.insight_repo = InsightRepository(self.db)

        # dependencies
        self.whatsapp_agent_manager = whatsapp_agent_manager

        # Use case
        self.get_agent_usecase = GetAgentUseCase(self.agent_repo, self.agent_conf_repo)
        self.create_agent_usecase = CreateAgentUseCase(
            self.agent_repo, self.agent_conf_repo
        )
        self.get_agent_analytic_usecase = GetAgentAnalyticsUseCase(self.analytic_repo)
        self.get_token_usage_trend_usecase = GetTokenUsageTrendUseCase(
            self.analytic_repo
        )
        self.get_message_usage_trend_usecase = GetMessageUsageTrendUseCase(
            self.analytic_repo
        )

        self.get_human_vs_ai_message_trend_usecase = GetHumanVsAiMessageTrendUseCase(
            self.analytic_repo
        )

        self.get_category_percentages_usecase = GetCategoryPercentages(
            self.analytic_repo
        )

        self.update_agent_usecase = UpdateAgentUseCase(
            self.agent_repo, self.agent_conf_repo, self.whatsapp_agent_manager
        )
        self.create_agent_obj_usecase = CreateAgentObjUseCase(
            self.agent_conf_repo,
            self.business_repo,
            self.document_knowladge_repo,
            self.business_knowladge_repo,
            self.whatsapp_agent_manager,
        )
        self.invoke_agent_usecase = InvokeAgentUseCase(
            self.analytic_repo,
            self.whatsapp_agent_manager,
            self.create_agent_obj_usecase,
        )
        self.generate_insight_usecase = GenerateInsight(
            self.insight_repo, self.business_repo, self.get_category_percentages_usecase
        )
        self.generate_gap_knowladge = GenerateGapKnowladge(
            self.business_repo, self.analytic_repo, self.insight_repo
        )
        super().__init__(__name__)

    async def get_agent(self) -> dict:
        user_id = current_user_id.get()
        user_email = current_user_email.get()

        self.logger.info(f"User {user_email}: Getting agent")
        if user_id is None:
            self.logger.warning("Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.get_agent_usecase.execute(GetAgentInput(agent_id=agent_id))
        if not result.is_success():
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError("Get agent usecase did not returned the data")

        self.logger.info(f"User {user_email}: Getting agent is successfully")
        return result_data.result_data

    async def create_new_agent(self, payload: CreateAgentIn):
        try:
            user_id = current_user_id.get()
            user_email = current_user_email.get()

            self.logger.info(f"User {user_email}: create new agent")
            if user_id is None:
                self.logger.warning(f"User {user_email}: Unauthorized Exception")
                raise UnauthorizedException()

            business_id, _ = (
                await self.business_repo.get_business_id_n_agent_id_by_user_id(user_id)
            )
            if business_id is None:
                self.logger.warning(f"User {user_email}: Business not found")
                raise BusinessNotFound()

            result = await self.create_agent_usecase.execute(
                CreateAgentUseCaseInput(business_id=business_id, agent_data=payload)
            )
            if not result.is_success():
                self.logger.error(
                    f"User {user_email}: Create new agent usecase is error"
                )
                self.raise_error_usecase(result)

            result_data = result.get_data()
            if result_data is None:
                raise RuntimeError("Create agent usecase did not returned the data")

            self.logger.info(f"User {user_email}: Create new agent is successfully")
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

    async def get_agent_analytic(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()

        self.logger.info(f"User {user_email}: get agent analytic")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            raise AgentNotFound()

        result = await self.get_agent_analytic_usecase.execute(
            GetAgentAnalyticsInput(agent_id=agent_id)
        )
        if not result.is_success():
            self.logger.error(f"User {user_email}: Get agent analytic usecase is error")
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError("Get analytic usecase did not returned the data")

        self.logger.info(f"User {user_email}: get agent analytic is successfully")
        return result_data

    async def get_token_usage_trend(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get token usage trend")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.get_token_usage_trend_usecase.execute(
            GetTokenUsageTrendInput(agent_id=agent_id)
        )
        if not result.is_success():
            self.logger.error(
                f"User {user_email}: Get token usage trend usecase is error"
            )
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError(
                "Get token usage trend usecase did not returned the data"
            )
        self.logger.info(f"User {user_email}: get token usage trend is successfully")
        return result_data

    async def get_message_usage_trend(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get message usage trend")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.get_message_usage_trend_usecase.execute(
            GetMessageUsageTrendInput(agent_id=agent_id)
        )
        if not result.is_success():
            self.logger.error(f"User {user_email}: Get message trend usecase is error")
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError(
                "Get message usage trend usecase did not returned the data"
            )
        self.logger.info(f"User {user_email}: get message usage trend is successfully")
        return result_data

    async def get_human_vs_ai_message_trend(self, period: str = "weekly"):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get human vs ai message trend")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized Exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: agent not found")
            raise AgentNotFound()

        result = await self.get_human_vs_ai_message_trend_usecase.execute(
            GetHumanVsAiMessageTrendInput(agent_id=agent_id, period=period)
        )
        if not result.is_success():
            self.logger.error(
                f"User {user_email}: Get human vs ai message trend usecase is error"
            )
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError(
                "Get human vs ai message trend usecase did not returned the data"
            )
        self.logger.info(
            f"User {user_email}: get human vs ai message trend is successfully"
        )
        return result_data

    async def get_category_percentages(self, period: str = "alltime"):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get category percentages")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.get_category_percentages_usecase.execute(
            GetCategoryPercentagesInput(agent_id=agent_id, period=period)
        )
        if not result.is_success():
            self.logger.error(
                f"User {user_email}: get category percentages usecase is error"
            )
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError(
                "Get category percentages usecase did not returned the data"
            )
        self.logger.info(f"User {user_email}: get category percentages is successfully")

        return result_data

    async def get_insight(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get insight")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        business_id, _ = await self.business_repo.get_business_id_n_agent_id_by_user_id(
            user_id
        )
        if business_id is None:
            self.logger.warning(f"User {user_email}: business not found")
            raise BusinessNotFound()

        insight = await self.insight_repo.get_current_insight(business_id)
        if insight is None:
            self.logger.warning(f"User {user_email}: Insight not found")
            raise InsightNotFound()

        self.logger.info(f"User {user_email}: get insight is sucessfully")

        return insight

    async def get_status_agent(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get status agent")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: agent not found")
            raise AgentNotFound()

        status = await self.agent_repo.get_status_agent(agent_id)
        if status is None:
            raise AgentNotFound()
        self.logger.info(f"User {user_email}: get status agent is successfully")
        return status

    async def update_status_agent(self, status: bool):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: update status agent")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        agent_id = await self.agent_repo.get_agent_id_by_user_id(user_id)
        if agent_id is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        updated_agent = await self.agent_repo.update_status_agent(agent_id, status)
        if updated_agent is None:
            self.logger.warning(f"User {user_email}: Agent not found")

            raise AgentNotFound()
        self.logger.info(f"User {user_email}: update status agent is successfully")
        return updated_agent

    async def update_agent(self, payload: UpdateAgentIn):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: update agent")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        agent = await self.agent_repo.get_agent_by_user_id(user_id)

        if agent is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.update_agent_usecase.execute(
            UpdateAgentInput(
                agent_id=agent.id,
                phone_number_id=agent.phone_number_id,
                agent_data=payload,
            )
        )

        if not result.is_success():
            self.logger.error(f"User {user_email}: update agent usecase is error")
            self.raise_error_usecase(result)

        result_data = result.get_data()

        if result_data is None:
            raise RuntimeError("Update agent usecase did not returned the data")
        self.logger.info(f"User {user_email}: Update agent is successfully")
        return result_data.result_data

    async def invoke_agent(self, text_message: str):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        agent = await self.agent_repo.get_agent_by_user_id(user_id)
        if agent is None:
            self.logger.warning(f"User {user_email}: Agent not found")
            raise AgentNotFound()

        result = await self.invoke_agent_usecase.execute(
            InvokeAgentInput(
                agent.phone_number_id,
                agent.business_id,
                agent.id,
                str(agent.business_id),
                WhatsappAgentState(messages=[], user_message=text_message),
            )
        )

        if not result.is_success():
            self.logger.error(f"User {user_email}: invoke agent usecase is error")
            self.raise_error_usecase(result)

        result_data = result.get_data()
        if result_data is None:
            raise RuntimeError("Invoke agent usecase did not returned the data")

        self.logger.info(f"User {user_email}: invoke agent is successfully")
        return result_data

    async def triger_insight_generator(self):
        user_id = current_user_id.get()
        if user_id is None:
            raise UnauthorizedException()

        business_id, agent_id = (
            await self.business_repo.get_business_id_n_agent_id_by_user_id(user_id)
        )
        if business_id is None:
            raise BusinessNotFound()

        if agent_id is None:
            raise AgentNotFound()

        queue_id = uuid4()
        payload_queue = {
            "queue_id": str(queue_id),
            "type": "generate_insight",
            "retry": 0,
            "job_payload": {"business_id": str(business_id), "agent_id": str(agent_id)},
        }
        self.redis_queue.enqueue(payload_queue)

        # usecase_result = await self.generate_insight_usecase.execute(
        #     GenerateInsightInput(business_id=business_id, agent_id=agent_id)
        # )
        # if not usecase_result.is_success():
        #     self.raise_error_usecase(usecase_result)

        # result_data = usecase_result.get_data()
        # if not result_data:
        #     raise RuntimeError("Generate insight usecase did not returned the data")

        return

    async def triger_knowladge_gap(self):
        user_id = current_user_id.get()
        if user_id is None:
            raise UnauthorizedException()

        business_id, agent_id = (
            await self.business_repo.get_business_id_n_agent_id_by_user_id(user_id)
        )
        if business_id is None:
            raise BusinessNotFound()

        if agent_id is None:
            raise AgentNotFound()

        usecase_result = await self.generate_gap_knowladge.execute(
            GenerateGapKnowladgeInput(business_id=business_id, agent_id=agent_id)
        )

        if not usecase_result.is_success():
            self.raise_error_usecase(usecase_result)

        result_data = usecase_result.get_data()
        if not result_data:
            raise RuntimeError(
                "Generate gap knowladge usecase did not returned the data"
            )

        return result_data

    async def get_knowladge_gap(self):
        user_id = current_user_id.get()
        user_email = current_user_email.get()
        self.logger.info(f"User {user_email}: get knowladge gap")
        if user_id is None:
            self.logger.warning(f"User {user_email}: Unauthorized exception")
            raise UnauthorizedException()

        business_id, _ = await self.business_repo.get_business_id_n_agent_id_by_user_id(
            user_id
        )
        if business_id is None:
            raise BusinessNotFound()

        knowladge_gap = await self.insight_repo.get_current_gap(business_id)
        self.logger.info(f"User {user_email}: get knowladge gap is successfully")
        return knowladge_gap
