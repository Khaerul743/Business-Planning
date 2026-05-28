from supabase import AsyncClient
from src.domain.repositories import (
    AnalyticsRepository,
    BusinessRepository,
    InsightRepository,
)
from src.domain.usecases.insight import (
    GenerateGapKnowladge,
    GenerateGapKnowladgeInput,
)
from .base import BaseJob, BaseJobHandler


class GenerateGapKnowladgeHandler(BaseJobHandler):
    def __init__(self, db: AsyncClient):
        self.db = db

        # Repositories
        self.analytic_repo = AnalyticsRepository(self.db)
        self.business_repo = BusinessRepository(self.db)
        self.insight_repo = InsightRepository(self.db)

        # usecase
        self.generate_gap_knowladge_usecase = GenerateGapKnowladge(
            self.business_repo, self.analytic_repo, self.insight_repo
        )

    async def handle(self, job: BaseJob) -> None:
        payload = job.job_payload
        await self.generate_gap_knowladge_usecase.execute(
            GenerateGapKnowladgeInput(
                payload["business_id"], agent_id=payload["agent_id"]
            )
        )
        return
