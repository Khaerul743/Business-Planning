from fastapi import APIRouter, Depends, Request, Response, status

from pydantic import BaseModel
from src.app.controllers import WhatsappController
from src.app.validators.whatsapp_schema import WebhookPayload, SendMessagePayload
from src.core.exceptions import TokenIsNotVerified, WhatsappBadRequest
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.infrastructure.meta.wa_manager import whatsapp_manager
from src.app.websocket.connection_manager import manager
from src.app.validators.wa_service_schema import WhatsappEventPayload

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp"])

get_whatsapp_controller = controller_factory(WhatsappController)


@router.get("/webhook", status_code=status.HTTP_200_OK)
def verify_webhook(
    request: Request,
):
    try:
        result = whatsapp_manager.verify_webhook(request)
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
    # print(payload)
    # return {"status": "oke"}


@router.post("/event")
async def whatsapp_event(payload: WhatsappEventPayload):

    business_id = payload.business_id

    await manager.send_to_business(
        business_id,
        payload.model_dump()
    )

    return {"success": True}


class CreateSessionPayload(BaseModel):
    business_id: str

@router.post("/session")
async def create_session(
    payload: CreateSessionPayload,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    business_id = payload.business_id
    result = await controller.create_session_controller(business_id)
    return success_response(result)

@router.get("/session/{business_id}")
async def get_session_status(
    business_id: str,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.get_session_status(business_id)
    return success_response(result)

@router.get("/all/session")
async def get_all_session(
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.get_all_session()
    return success_response(result)

@router.delete("/session/{business_id}")
async def delete_session(
    business_id: str,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.delete_session(business_id)
    return success_response(result)

@router.post("/session/reconnect/{business_id}")
async def reconnect_session(
    business_id: str,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.reconnect_session(business_id)
    return success_response(result)

@router.post("/message/send/{business_id}")
async def send_message(
    payload: SendMessagePayload,
    controller: WhatsappController = Depends(get_whatsapp_controller),
):
    result = await controller.send_message_controller(payload)
    return success_response(result)

