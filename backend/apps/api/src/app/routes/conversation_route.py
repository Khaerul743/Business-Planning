from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.app.controllers import ConversationController
from src.app.middlewares.rbac import require_roles
from src.app.validators.message_schema import InsertDirectMessage
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/conversation", tags=["conversation"])

get_conversation_controller = controller_factory(ConversationController)


@router.get("/me/all", status_code=status.HTTP_200_OK)
async def get_all_conversations(
    page: int = 1,
    limit: int = 10,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_all_conversation_handler(page=page, limit=limit)
    return success_response(result, "Get all conversation is successfully")


@router.get("/me/message/{conversation_id}", status_code=status.HTTP_200_OK)
async def get_all_messages(
    conversation_id: UUID,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_all_messages_handler(conversation_id)
    return success_response(result, "Get all messages is successfully")


@router.get("/me/fallback/all", status_code=status.HTTP_200_OK)
async def get_all_conversation_fallback(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_all_conversation_human_fallback_handler()
    return success_response(
        result, "Get all conversation with human fallback is successfully"
    )


@router.get("/me/fallback/{conversation_id}", status_code=status.HTTP_200_OK)
async def get_conversation_fallback(
    conversation_id: UUID,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_conversation_fallback_handler(conversation_id)
    return success_response(
        result, "Get all conversation with human fallback is successfully"
    )


@router.post("/message/post/{conversation_id}")
async def post_message(
    conversation_id: UUID,
    text_message: InsertDirectMessage,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.post_direct_message_handler(
        conversation_id, text_message.text_message
    )
    return success_response(result, "Post direct message is successfully")


@router.get("/agent/status/{conversation_id}")
async def get_customer_status_agent(
    conversation_id: UUID,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_customer_status_agent_handler(conversation_id)
    return success_response(result, "get customer status agent message is successfully")


@router.put("/agent/status/{conversation_id}")
async def update_customer_status_agent(
    conversation_id: UUID,
    status: bool,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.update_customer_status_agent_handler(
        conversation_id, status
    )
    return success_response(
        result, "Update customer status agent message is successfully"
    )


@router.delete("/me/fallback/{conversation_id}", status_code=status.HTTP_200_OK)
async def delete_conversation_fallback(
    conversation_id: UUID,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.delete_conversation_fallback_handler(conversation_id)
    return success_response(result, "Delete conversation fallback is successfully")
