from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models import WhatsappChannel


class IWhatsappChannelRepository(ABC):
    @abstractmethod
    async def get_whatsapp_channel_by_business_id(self, business_id: UUID)-> list[WhatsappChannel] | None:
        pass

    @abstractmethod
    async def save_whatsapp_channel(self, payload: dict) -> None:
        pass