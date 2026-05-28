from fastapi import APIRouter, Depends, status

from src.app.controllers import AgentController
from src.app.middlewares.rbac import require_roles
from src.app.validators.agent_schema import CreateAgentIn, UpdateAgentIn, InvokeAgentIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/agent", tags=["agent"])

get_agent_controller = controller_factory(AgentController)


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_agent(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_agent_handler()
    return success_response(result, "Create new agent is successfully")


@router.post("", status_code=status.HTTP_200_OK)
async def create_agent(
    payload: CreateAgentIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.create_new_agent_handler(payload)
    return success_response(result, "Create new agent is successfully")


@router.post("/invoke/me", status_code=status.HTTP_200_OK)
async def invoke_agent(
    payload: InvokeAgentIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.invoke_agent_handler(payload.text_message)
    return success_response(result, "invoke agent is successfully")


@router.put("/me", status_code=status.HTTP_200_OK)
async def update_agent(
    payload: UpdateAgentIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.update_agent_handler(payload)
    return success_response(result, "Update agent is successfully")


@router.get("/analytic/me", status_code=status.HTTP_200_OK)
async def get_analytic_agent(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_agent_analytic()
    return success_response(result, "Get analytic agent is successfully")


@router.get("/analytic/token-usage-trend/me", status_code=status.HTTP_200_OK)
async def get_token_usage_trend(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_token_usage_trend_handler()
    return success_response(result, "Get token usage trend is successfully")


@router.get("/analytic/message-usage-trend/me", status_code=status.HTTP_200_OK)
async def get_message_usage_trend(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_message_usage_trend_handler()
    return success_response(result, "Get message usage trend is successfully")


@router.get(
    "/analytic/message-trend/human-vs-ai/{period}/me", status_code=status.HTTP_200_OK
)
async def get_human_vs_ai_message_trend(
    period: str,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_human_vs_ai_message_trend_handler(period)
    return success_response(result, "Get human vs ai message trend is successfully")


@router.get(
    "/analytic/category-percentages/{period}/me", status_code=status.HTTP_200_OK
)
async def get_category_percentages(
    period: str,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    """
    Get message category percentages based on period.
    - period: `day` (last 24 hours), `weekly` (last 7 days), `alltime`
    """
    result = await controller.get_category_percentages_handler(period)
    return success_response(result, "Get category percentages is successfully")


@router.get("/analytic/insight", status_code=status.HTTP_200_OK)
async def get_insight(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_insight_handler()
    return success_response(result, "get insight is successfully")


@router.get("/status/me", status_code=status.HTTP_200_OK)
async def get_status_agent(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_status_agent_handler()
    return success_response(result, "get status agent is successfully")


@router.put("/status/me", status_code=status.HTTP_200_OK)
async def update_status_agent(
    status: bool,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.update_status_agent_handler(status)
    return success_response(result, "Update status agent is successfully")


@router.get("/insight", status_code=status.HTTP_200_OK)
async def insight(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.insight_handler()
    return success_response(result, "Update status agent is successfully")


@router.get("/analytic/knowlage_gap", status_code=status.HTTP_200_OK)
async def get_knowlage_gap(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: AgentController = Depends(get_agent_controller),
):
    result = await controller.get_knowladge_gap_handler()
    return success_response(result, "get knowladge gap is successfully")


# @router.get("/knowlage_gap/trigger", status_code=status.HTTP_200_OK)
# async def trigger_knowlage_gap(
#     _: None = Depends(jwtHandler.jwt_required),
#     __: None = Depends(require_roles("admin", "user")),
#     controller: AgentController = Depends(get_agent_controller),
# ):
#     result = await controller.triger_gap_knowladge_handler()
#     return success_response(result, "Generate knowladge gap is successfully")
