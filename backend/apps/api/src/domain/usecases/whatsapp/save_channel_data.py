from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from src.domain.usecases.base import BaseUseCase, UseCaseResult
from src.domain.usecases.interfaces import IWhatsappChannelRepository

@dataclass
class SaveChannelDataInput:
    business_id: UUID
    phone_number: str
    status: str
    display_name: str | None = None

@dataclass
class SaveChannelDataOutput:
    data: dict

class SaveChannelDataUseCase(
    BaseUseCase[SaveChannelDataInput, SaveChannelDataOutput]
):
    def __init__(self, channel_repo: IWhatsappChannelRepository):
        self.channel_repo = channel_repo

    async def execute(self, input_data: SaveChannelDataInput) -> UseCaseResult[SaveChannelDataOutput]:
        try:
            channels = await self.channel_repo.get_whatsapp_channel_by_business_id(input_data.business_id)
            existing_channel = channels[0] if channels else None
            
            payload = {
                "business_id": str(input_data.business_id),
                "phone_number": input_data.phone_number,
                "display_name": input_data.display_name,
                "status": input_data.status,
            }
            
            if existing_channel:
                payload["id"] = str(existing_channel.id)
            
            if input_data.status == "connected":
                if not existing_channel or not existing_channel.connected_at:
                    payload["connected_at"] = datetime.now(timezone.utc).isoformat()
            elif existing_channel and existing_channel.connected_at:
                payload["connected_at"] = existing_channel.connected_at.isoformat()
            
            await self.channel_repo.save_whatsapp_channel(payload)
            
            return UseCaseResult.success_result(SaveChannelDataOutput(data=payload))
        except Exception as e:
            return UseCaseResult.error_result(f"Failed to save channel data: {e}", e)
