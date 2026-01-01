from fastapi import APIRouter, Depends, status

from src.app.controllers import AgentController
from src.app.middlewares.rbac import require_roles
from src.app.validators.agent_schema import CreateAgentIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/agent", tags=["agent"])

get_business_knowladge_controller = controller_factory(AgentController)


@router.post("", status_code=status.HTTP_200_OK)
async def get_all_business_knowladge_by_business_id(
    payload: CreateAgentIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_business_knowladge_controller),
):
    result = await controller.create_new_agent_handler(payload)
    return success_response(result, "Create new agent is successfully")
