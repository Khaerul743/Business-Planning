from dataclasses import dataclass
from uuid import UUID

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import ICustomerRepository


@dataclass
class GetCustomersInput:
    agent_id: UUID


@dataclass
class GetCustomersOutput:
    total_customers: int
    customers: list[dict]


class GetCustomers(BaseUseCase[GetCustomersInput, GetCustomersOutput]):
    def __init__(self, customer_repo: ICustomerRepository):
        self.customer_repo = customer_repo

    async def execute(
        self, input_data: GetCustomersInput
    ) -> UseCaseResult[GetCustomersOutput]:
        try:
            customers = await self.customer_repo.get_all_customer_by_agent_id(
                input_data.agent_id
            )

            # Format list of model objects to dicts explicitly mapped
            customer_list = [customer.model_dump() for customer in customers]
            total_customers = len(customer_list)

            return UseCaseResult.success_result(
                GetCustomersOutput(
                    total_customers=total_customers, customers=customer_list
                )
            )
        except Exception as e:
            return UseCaseResult.error_result(
                f"Unexpected error while getting customers: {e}", e
            )
