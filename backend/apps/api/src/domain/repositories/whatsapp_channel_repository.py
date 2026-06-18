from uuid import UUID

from supabase import AsyncClient
from src.domain.usecases.interfaces import IWhatsappChannelRepository
from src.core.utils.logger import get_logger
from src.domain.models import WhatsappChannel

class WhatsappChannelRepository(IWhatsappChannelRepository):
    def __init__(self,db: AsyncClient):
        self.db = db
        self._logger = get_logger(__name__)

    async def get_whatsapp_channel_by_business_id(self, business_id: UUID) -> list[WhatsappChannel] | None:
        try:
            result = await self.db.table("Whatsapp_channels").select("*").eq("business_id", str(business_id)).execute()
            if len(result.data) == 0:
                return None
            
            result_data = [WhatsappChannel.model_validate(i) for i in result.data]
            return result_data
        except Exception as e:
            self._logger.error(f"Error while get whatsapp channel by business id: {e}")
            raise e

    async def save_whatsapp_channel(self, payload: dict) -> None:
        try:
            await self.db.table("Whatsapp_channels").upsert(payload).execute()
        except Exception as e:
            self._logger.error(f"Error while save whatsapp channel: {e}")
            raise e