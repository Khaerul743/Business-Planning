from supabase import AsyncClient

from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.core.context.request_context import current_user_id
from src.core.exceptions.auth_exception import UnauthorizedException
from src.core.exceptions.business_exception import (
    BusinessNotFound,
    BusinessPermissionNeeded,
)
from src.domain.repositories import (
    BusinessKnowladgeRepository,
    BusinessRepository,
    UserRepository,
)

from .base import BaseService


class BusinessKnowladgeService(BaseService):
    def __init__(self, db: AsyncClient):
        self.db = db

        self.user_repo = UserRepository(self.db)
        self.business_knowladge_repo = BusinessKnowladgeRepository(self.db)
        self.business_repo = BusinessRepository(self.db)

        super().__init__(__name__)

    async def _get_business_id(self, user_id: int) -> int | None:
        business_id = await self.business_repo.get_business_id_by_user_id(user_id)
        return business_id

    async def get_all_business_knowladge_by_business_id(self):
        try:
            user_id = current_user_id.get()
            if user_id is None:
                raise UnauthorizedException()
            business_id = await self._get_business_id(user_id)
            if business_id is None:
                raise BusinessNotFound()

            business_knowladges = await self.business_knowladge_repo.get_all_business_knowladge_by_business_id(
                business_id
            )

            return business_knowladges
        except BusinessNotFound as e:
            self.logger.warning(str(e))
            raise e
        except BusinessPermissionNeeded as e:
            self.logger.warning(
                f"Don't have permission business id {business_id}: {str(e)}"
            )
            raise e

    async def add_business_knowladge(self, payload: AddBusinessKnowladgeIn):
        try:
            user_id = current_user_id.get()
            if user_id is None:
                raise UnauthorizedException()
            business_id = await self._get_business_id(user_id)
            if business_id is None:
                raise BusinessNotFound()

            response_data = await self.business_knowladge_repo.add_business_knowladge(
                business_id, payload
            )
            return response_data
        except BusinessNotFound as e:
            self.logger.warning(str(e))
            raise e

    async def update_business_knowladge(
        self, business_knowladge_id: int, payload: UpdateBusinessKnowladgeIn
    ):
        user_id = current_user_id.get()
        if user_id is None:
            raise UnauthorizedException()
        business = await self._get_business_id(user_id)
        if business is None:
            raise BusinessNotFound()
        response_data = (
            await self.business_knowladge_repo.update_business_knowladge_by_id(
                business_knowladge_id, payload
            )
        )
        return response_data

    async def delete_business_knowladge(self, business_knowladge_id: int):
        user_id = current_user_id.get()
        if user_id is None:
            raise UnauthorizedException()

        business_id = await self._get_business_id(user_id)
        if business_id is None:
            raise BusinessNotFound()

        result = await self.business_knowladge_repo.delete_business_knowladge_by_id(
            business_id, business_knowladge_id
        )

        return result
