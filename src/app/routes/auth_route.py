from fastapi import APIRouter, Depends, Request, Response, status

from src.app.controllers import AuthController
from src.app.validators.auth_schema import LoginIn, RegisterIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import auth_success_response, success_response

router = APIRouter(prefix="/api/auth", tags=["auth"])

get_auth_controller = controller_factory(AuthController)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    payload: RegisterIn,
    controller: AuthController = Depends(get_auth_controller),
):
    result = await controller.register_new_user(payload)
    data = result.model_dump()
    return success_response(
        data, "Register new user is successfully", status.HTTP_201_CREATED
    )


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    payload: LoginIn,
    controller: AuthController = Depends(get_auth_controller),
):
    result = await controller.login_handler(response, payload)
    data = result.model_dump()
    return auth_success_response(response, data, "Login is successfully")


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    controller: AuthController = Depends(get_auth_controller),
):
    result = await controller.refresh_token_handler(request, response)
    return auth_success_response(response, result, "Access token has been updated")


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    response: Response,
    controller: AuthController = Depends(get_auth_controller),
):
    result = await controller.logout_handler(response)
    return auth_success_response(response, result, "Logout is successfully")
