from abc import ABC, abstractmethod

from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.domain.models import BusinessKnowladge


class IBusinessKnowladgeRepository(ABC):
    @abstractmethod
    async def get_all_business_knowladge_by_business_id(
        self, business_id: int
    ) -> list[BusinessKnowladge] | None:
        pass

    @abstractmethod
    async def add_business_knowladge(
        self, business_id: int, business_knowladge_data: AddBusinessKnowladgeIn
    ) -> BusinessKnowladge:
        pass

    @abstractmethod
    async def update_business_knowladge_by_id(
        self,
        business_knowladge_id: int,
        business_knowladge_data: UpdateBusinessKnowladgeIn,
    ) -> BusinessKnowladge:
        pass

    @abstractmethod
    async def delete_business_knowladge_by_id(
        self, business_id: int, business_knowladge_id: int
    ) -> BusinessKnowladge:
        pass
