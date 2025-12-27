from dataclasses import dataclass

from src.app.validators.business_schema import AddBusinessIn
from src.domain.models import Business
from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IBusinessRepository


@dataclass
class AddBusinessInput:
    user_id: int
    business_data: AddBusinessIn


@dataclass
class AddBusinessOutput:
    business_data: Business


class AddBusiness(BaseUseCase[AddBusinessInput, AddBusinessOutput]):
    def __init__(self, business_repository: IBusinessRepository):
        self.business_respository = business_repository

    async def execute(
        self, input_data: AddBusinessInput
    ) -> UseCaseResult[AddBusinessOutput]:
        try:
            result = await self.business_respository.add_business(
                input_data.user_id, input_data.business_data
            )
            return UseCaseResult.success_result(AddBusinessOutput(result))
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpexted error while add new business: {str(e)}", e
            )
