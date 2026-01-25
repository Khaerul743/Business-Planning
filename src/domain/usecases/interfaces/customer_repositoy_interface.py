from abc import ABC, abstractmethod

from src.app.validators.customer_schema import InsertNewCustomer
from src.domain.models import Customers


class ICustomerRepository(ABC):
    @abstractmethod
    async def get_or_insert_custormer(
        self, agent_id: int, customer_data: InsertNewCustomer
    ) -> Customers:
        pass

    @abstractmethod
    async def get_all_customer_by_business_id(
        self, business_id: int
    ) -> list[Customers]:
        pass
