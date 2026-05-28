from uuid import UUID

from supabase import AsyncClient

from src.app.validators.customer_schema import InsertNewCustomer
from src.domain.models import Customers
from src.domain.usecases.interfaces import ICustomerRepository


class CustomerRepository(ICustomerRepository):
    def __init__(self, db: AsyncClient):
        self.db = db

    async def get_or_insert_custormer(
        self, agent_id: UUID, customer_data: InsertNewCustomer
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
            payload["agent_id"] = str(agent_id)
            result = await self.db.table("Customers").insert(payload).execute()
            return Customers.model_validate(result.data[0])
        return Customers.model_validate(customer.data)

    async def get_all_customer_by_business_id(
        self, business_id: UUID
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

    async def get_phone_number_by_conversation_id(
        self, conversation_id: UUID
    ) -> str | None:
        result = await (
            self.db.table("Conversations")
            .select("Customers(phone_number)")
            .eq("id", conversation_id)
            .maybe_single()
            .execute()
        )

        if result is None:
            return None

        return result.data["Customers"]["phone_number"]

    async def get_customer_status_agent_by_agent_id(
        self, agent_id: UUID
    ) -> bool | None:
        result = (
            await self.db.table("Customers")
            .select("enable_ai")
            .eq("agent_id", agent_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None
        return result.data["enable_ai"]

    async def get_customer_status_agent_by_customer_id(
        self, customer_id: UUID
    ) -> bool | None:
        result = await (
            self.db.table("Customers")
            .select("enable_ai")
            .eq("id", customer_id)
            .maybe_single()
            .execute()
        )
        if result is None:
            return None

        return result.data["enable_ai"]

    async def update_customer_status_agent_by_customer_id(
        self, customer_id: UUID, status: bool
    ) -> Customers | None:
        result = await (
            self.db.table("Customers")
            .update({"enable_ai": status})
            .eq("id", customer_id)
            .execute()
        )

        if len(result.data) == 0:
            return None

        return Customers.model_validate(result.data[0])

    async def get_all_customer_by_agent_id(self, agent_id: UUID) -> list[Customers]:
        result = await (
            self.db.table("Customers").select("*").eq("agent_id", agent_id).execute()
        )
        return [Customers.model_validate(item) for item in result.data]
