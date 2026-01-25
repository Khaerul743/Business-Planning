from fastapi import APIRouter, Depends, status

from src.app.controllers import ConversationController
from src.app.middlewares.rbac import require_roles
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/conversation", tags=["business"])

get_conversation_controller = controller_factory(ConversationController)


@router.get("/me/all", status_code=status.HTTP_200_OK)
async def get_all_conversations(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_all_conversation_handler()
    return success_response(result, "Get all conversation is successfully")


@router.get("/me/message/{conversation_id}", status_code=status.HTTP_200_OK)
async def get_all_messages(
    conversation_id: int,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: ConversationController = Depends(get_conversation_controller),
):
    result = await controller.get_all_messages_handler(conversation_id)
    return success_response(result, "Get all messages is successfully")
