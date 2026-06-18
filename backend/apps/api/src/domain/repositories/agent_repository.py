from uuid import UUID

from supabase import AsyncClient

from src.app.validators.agent_schema import InsertAgent
from src.domain.models import Agents
from src.domain.usecases.interfaces import IAgentRepository
from src.core.utils.logger import get_logger


class AgentRepository(IAgentRepository):
    def __init__(self, db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def get_agent_by_phone_number_id(self, phone_number_id: str) -> Agents | None:
        try:
            result = (
                await self.db.table("Agents")
                .select("*")
                .eq("phone_number_id", phone_number_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None

            return Agents.model_validate(result.data)
        except Exception as e:
            self._logger.error(f"Error while get agent by phone number id: {str(e)}")
            raise e

    async def get_agent_by_user_id(self, user_id: UUID) -> Agents | None:
        try:
            result = (
                await self.db.table("Businesses")
                .select(
                    "Agents(id, business_id, name, phone_number_id, created_at, updated_at)"
                )
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
                
            return Agents.model_validate(result.data["Agents"][0])
        except Exception as e:
            self._logger.error(f"Error while get agent by user id: {str(e)}")
            raise e

    async def get_agent_by_id(self, id: UUID) -> Agents | None:
        try:
            result = (
                await self.db.table("Agents")
                .select("*")
                .eq("id", id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
            return Agents.model_validate(result.data)
        except Exception as e:
            self._logger.error(f"Error while get agent by id: {str(e)}")
            raise e

    async def get_agent_id_by_user_id(self, user_id: UUID) -> UUID | None:
        try:
            result = (
                await self.db.table("Businesses")
                .select("Agents(id)")
                .eq("user_id", user_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
            return result.data["Agents"][0]["id"]
        except Exception as e:
            self._logger.error(f"Error while get agent id by user id: {str(e)}")
            raise e

    async def get_agent_by_business_id(self, business_id: UUID) -> Agents | None:
        try:
            result = (
                await self.db.table("Agents")
                .select("*")
                .eq("business_id", str(business_id))
                .maybe_single()
                .execute()
            )
            if result is None:
                return None
            return Agents.model_validate(result.data)
        except Exception as e:
            self._logger.error(f"Error while get agent by business id: {str(e)}")
            raise e

    async def get_status_agent(self, agent_id: UUID) -> bool | None:
        try:
            result = await (
                self.db.table("Agents")
                .select("enable_ai")
                .eq("id", agent_id)
                .maybe_single()
                .execute()
            )
            if result is None:
                return None

            return result.data["enable_ai"]
        except Exception as e:
            self._logger.error(f"Error while get status agent: {str(e)}")
            raise e

    async def create_agent_by_business_id(
        self, business_id: UUID, agent_data: InsertAgent
    ) -> Agents:
        try:
            payload = agent_data.model_dump()
            payload["business_id"] = str(business_id)
            del payload["fallback_to_human"]


            result = await self.db.table("Agents").insert(payload).execute()

            return Agents.model_validate(result.data[0])
        except Exception as e:
            self._logger.error(f"Error while create agent by business id: {str(e)}")
            raise e

    async def update_status_agent(self, agent_id: UUID, status: bool) -> Agents | None:
        try:
            result = (
                await self.db.table("Agents")
                .update({"enable_ai": status})
                .eq("id", agent_id)
                .execute()
            )
            if len(result.data) == 0:
                return None

            return Agents.model_validate(result.data[0])
        except Exception as e:
            self._logger.error(f"Error while update status agent: {str(e)}")
            raise e

    async def update_name_agent(self, agent_id: UUID, name: str) -> str:
        try:
            result = (
                await self.db.table("Agents")
                .update({"name": name})
                .eq("id", agent_id)
                .execute()
            )
            return name
        except Exception as e:
            self._logger.error(f"Error while update name agent: {str(e)}")
            raise e
