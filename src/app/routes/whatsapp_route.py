from fastapi import APIRouter, Depends, Request, Response, status

from src.app.controllers import WhatsappController
from src.app.validators.whatsapp_schema import WebhookPayload
from src.core.exceptions import TokenIsNotVerified, WhatsappBadRequest
from src.core.utils.factory import controller_factory

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

get_whatsapp_controller = controller_factory(WhatsappController)


@router.get("/webhook", status_code=status.HTTP_200_OK)
def verify_webhook(
    request: Request,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    try:
        result = controller.whatsapp_service.whatsapp_manager.verify_webhook(request)
        return result

    except WhatsappBadRequest as e:
        raise e
    except TokenIsNotVerified as e:
        raise e
    except Exception as e:
        raise e


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def receive_webhook(
    payload: WebhookPayload,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.send_message(payload)
    return result
