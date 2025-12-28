from fastapi import APIRouter, Depends, status

from src.app.controllers import BusinessKnowladgeController
from src.app.middlewares.rbac import require_roles
from src.app.validators.business_knowladge_schema import AddBusinessKnowladgeIn
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/business_knowladge", tags=["business"])

get_business_knowladge_controller = controller_factory(BusinessKnowladgeController)


@router.get("/business_id", status_code=status.HTTP_201_CREATED)
async def add_business_knowladge(
    business_id: int,
    payload: AddBusinessKnowladgeIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessKnowladgeController = Depends(
        get_business_knowladge_controller
    ),
):
    result = await controller.add_business_knowladge_handler(business_id, payload)
    return success_response(result, "Add new business knowladge is successfully")
