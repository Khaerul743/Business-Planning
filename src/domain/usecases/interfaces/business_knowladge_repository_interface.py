from abc import ABC, abstractmethod

from src.app.validators.business_knowladge_schema import AddBusinessKnowladgeIn
from src.domain.models import BusinessKnowladge


class IBusinessKnowladgeRepository(ABC):
    @abstractmethod
    async def add_business_knowladge(
        self, business_id: int, business_knowladge_data: AddBusinessKnowladgeIn
    ) -> BusinessKnowladge:
        pass
