# from datetime import datetime
# from dataclasses import dataclass
# from src.domain.usecases.base import BaseUseCase, UseCaseResult
# from src.domain.usecases.interfaces import IAnalyticRepository
# from src.app.validators.analytic_schema import InsertAgentAnalytic

# @dataclass
# class InsertAgentAnalyticInput:
#     agent_id: int
#     analytic_data: InsertAgentAnalytic

# @dataclass
# class InsertAgentAnalyticOutput:
#     pass

# class InsertAgentAnalyticUseCase(BaseUseCase[InsertAgentAnalyticInput, InsertAgentAnalyticOutput]):
#     def __init__(self, analytic_repo: IAnalyticRepository):
#         self.analytic_repo = analytic_repo

#     async def execute(self, input_data: InsertAgentAnalyticInput) -> UseCaseResult[InsertAgentAnalyticOutput]:
#         try:
#             date_now = datetime.now().date()
#             result = self.analytic_repo.get_or_insert_agent_analytic()
