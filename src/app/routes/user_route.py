from fastapi import APIRouter, Depends, status

from src.app.controllers import UserController
from src.app.middlewares.rbac import require_roles
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/user", tags=["users"])

get_user_controller = controller_factory(UserController)


@router.get("/me")
async def get_me(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("user", "admin")),
    controller: UserController = Depends(get_user_controller),
):
    result = await controller.get_current_user()
    result_data = result.model_dump()

    return success_response(result_data)
