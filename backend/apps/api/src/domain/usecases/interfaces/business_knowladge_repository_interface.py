from abc import ABC, abstractmethod
from uuid import UUID

from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.domain.models import BusinessKnowladge


class IBusinessKnowladgeRepository(ABC):
    @abstractmethod
    async def get_all_business_knowladge_by_business_id(
        self, business_id: UUID
    ) -> list[BusinessKnowladge] | None:
        pass

    @abstractmethod
    async def add_business_knowladge(
        self, business_id: UUID, business_knowladge_data: AddBusinessKnowladgeIn
    ) -> BusinessKnowladge:
        pass

    @abstractmethod
    async def update_business_knowladge_by_id(
        self,
        business_knowladge_id: UUID,
        business_knowladge_data: UpdateBusinessKnowladgeIn,
    ) -> BusinessKnowladge:
        pass

    @abstractmethod
    async def delete_business_knowladge_by_id(
        self, business_id: UUID, business_knowladge_id: UUID
    ) -> BusinessKnowladge:
        pass
