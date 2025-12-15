from fastapi import APIRouter, Depends, Request, status

from src.app.controllers import AuthController
from src.app.validators.auth_schema import RegisterIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response

router = APIRouter(prefix="/api/auth", tags=["auth"])

get_auth_controller = controller_factory(AuthController)


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
    request: Request,
    payload: RegisterIn,
    controller: AuthController = Depends(get_auth_controller),
):
    result = await controller.register_new_user(payload)
    data = result.model_dump()
    return success_response(data, "Register new user is successfully")
