from fastapi import APIRouter, Depends, status

from src.app.controllers import BusinessKnowladgeController
from src.app.middlewares.rbac import require_roles
from src.app.validators.business_knowladge_schema import (
    AddBusinessKnowladgeIn,
    UpdateBusinessKnowladgeIn,
)
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/business_knowladge", tags=["business"])

get_business_knowladge_controller = controller_factory(BusinessKnowladgeController)


@router.get("/me/all", status_code=status.HTTP_200_OK)
async def get_all_business_knowladge_by_business_id(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessKnowladgeController = Depends(
        get_business_knowladge_controller
    ),
):
    result = await controller.get_all_business_knowladge_by_business_id_handler()
    return success_response(result, "Get all business knowladges is successfully")


@router.post("/me", status_code=status.HTTP_201_CREATED)
async def add_business_knowladge(
    payload: AddBusinessKnowladgeIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessKnowladgeController = Depends(
        get_business_knowladge_controller
    ),
):
    result = await controller.add_business_knowladge_handler(payload)
    return success_response(result, "Add new business knowladge is successfully")


@router.put("/me/{business_knowladge_id}", status_code=status.HTTP_200_OK)
async def update_business_knowladge(
    business_knowladge_id: int,
    payload: UpdateBusinessKnowladgeIn,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessKnowladgeController = Depends(
        get_business_knowladge_controller
    ),
):
    result = await controller.update_business_knowladge_handler(
        business_knowladge_id, payload
    )
    return success_response(result, "update business knowladge is successfully")


@router.delete("/me/{business_knowladge_id}", status_code=status.HTTP_200_OK)
async def delete_business_knowladge(
    business_knowladge_id: int,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: BusinessKnowladgeController = Depends(
        get_business_knowladge_controller
    ),
):
    result = await controller.delete_business_knowladge_handler(business_knowladge_id)
    return success_response(result, "delete business knowladge is successfully")
