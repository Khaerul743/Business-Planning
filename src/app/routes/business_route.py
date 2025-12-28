from fastapi import APIRouter, Depends, status

from src.app.controllers import BusinessController
from src.app.middlewares.rbac import require_roles
from src.app.validators.business_schema import AddBusinessIn, BusinessUpdateIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/business", tags=["business"])

get_business_controller = controller_factory(BusinessController)


@router.get("", status_code=status.HTTP_200_OK)
async def get_current_business(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessController = Depends(get_business_controller),
):
    result = await controller.get_current_business_handler()
    return success_response(result.model_dump(), "Get current business is successfully")


@router.post("", status_code=status.HTTP_201_CREATED)
async def add_business(
    payload: AddBusinessIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessController = Depends(get_business_controller),
):
    result = await controller.add_new_business_handler(payload)
    result_data = result.model_dump()

    return success_response(
        result_data, "Add new business is successfully", status.HTTP_201_CREATED
    )


@router.put("", status_code=status.HTTP_200_OK)
async def update_business(
    payload: BusinessUpdateIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessController = Depends(get_business_controller),
):
    result = await controller.update_business_handler(payload)
    result_data = result.model_dump()

    return success_response(
        result_data, "Update business is successfully", status.HTTP_200_OK
    )
