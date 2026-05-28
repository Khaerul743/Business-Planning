from supabase import AsyncClient
from src.domain.repositories import (
    InsightRepository,
    BusinessRepository,
    AnalyticsRepository,
)
from src.domain.usecases.analytic import GetCategoryPercentages
from src.domain.usecases.insight import GenerateInsight, GenerateInsightInput
from .base import BaseJob, BaseJobHandler


class GenerateInsightHandler(BaseJobHandler):
    def __init__(self, db: AsyncClient):
        self.db = db

        # Repositories
        self.insight_repo = InsightRepository(self.db)
        self.business_repo = BusinessRepository(self.db)
        self.analytic_repo = AnalyticsRepository(self.db)

        # Usecases
        self.get_category_percentage_usecase = GetCategoryPercentages(
            self.analytic_repo
        )
        self.generate_insight_usecase = GenerateInsight(
            self.insight_repo, self.business_repo, self.get_category_percentage_usecase
        )

    async def handle(self, job: BaseJob):
        payload = job.job_payload
        await self.generate_insight_usecase.execute(
            GenerateInsightInput(
                business_id=payload["business_id"], agent_id=payload["agent_id"]
            )
        )
        return
