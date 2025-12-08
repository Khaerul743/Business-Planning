from fastapi import APIRouter, Request, Response, status

from src.app.controllers import WhatsappController
from src.app.validators.whatsapp_schema import WebhookPayload
from src.core.exceptions import TokenIsNotVerified, WhatsappBadRequest

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

controller = WhatsappController()


@router.get("/webhook", status_code=status.HTTP_200_OK)
def verify_webhook(request: Request):
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
def receive_webhook(payload: WebhookPayload):
    controller.send_message(payload)
    return {"status": "ok"}
