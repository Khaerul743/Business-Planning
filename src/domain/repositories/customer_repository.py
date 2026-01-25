from supabase import AsyncClient

from src.app.validators.customer_schema import InsertNewCustomer
from src.domain.models import Customers
from src.domain.usecases.interfaces import ICustomerRepository


class CustomerRepository(ICustomerRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_or_insert_custormer(
        self, agent_id: int, customer_data: InsertNewCustomer
    ) -> Customers:
        customer = await (
            self.db.table("Customers")
            .select("*")
            .eq("phone_number", customer_data.phone_number)
            .maybe_single()
            .execute()
        )
        if customer is None:
            payload = customer_data.model_dump()
            payload["agent_id"] = agent_id
            result = await self.db.table("Customers").insert(payload).execute()
            return Customers.model_validate(result.data[0])
        return Customers.model_validate(customer.data)

    async def get_all_customer_by_business_id(
        self, business_id: int
    ) -> list[Customers]:
        result = (
            await self.db.table("Businesses")
            .select("Agents(Customers(*))")
            .eq("id", business_id)
            .execute()
        )
        list_customers = result = result.data[0]["Agents"]["Customers"]
        customers = [Customers.model_validate(i) for i in list_customers]
        return customers
