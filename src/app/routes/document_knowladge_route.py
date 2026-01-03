from fastapi import APIRouter, Depends, Form, UploadFile, status

from src.app.controllers import DocumentKnowladgeController
from src.app.middlewares.rbac import require_roles
from src.core.utils.factory import controller_factory
from src.core.utils.response import success_response
from src.core.utils.security import jwtHandler

router = APIRouter(prefix="/api/document_knowladge", tags=["document_knowladge"])

get_document_knowladge_controller = controller_factory(DocumentKnowladgeController)


@router.get("/me/all", status_code=status.HTTP_200_OK)
async def get_all_document_knowladges(
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: DocumentKnowladgeController = Depends(
        get_document_knowladge_controller
    ),
):
    result = await controller.get_all_document_knowladges_handler()
    return success_response(result, "Get all document knowladges is successfully")


@router.post("/me", status_code=status.HTTP_201_CREATED)
async def add_document_knowladge(
    file: UploadFile,
    file_description: str = Form(...),
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: DocumentKnowladgeController = Depends(
        get_document_knowladge_controller
    ),
):
    result = await controller.add_document_to_agent_handler(file, file_description)
    return success_response(
        result,
        "Add document knowladge to agent is successfully",
        status.HTTP_201_CREATED,
    )


@router.delete("/me/{document_knowladge_id}", status_code=status.HTTP_200_OK)
async def delete_document_knowladge(
    document_knowladge_id: int,
    _: None = Depends(jwtHandler.jwt_required),
    __: None = Depends(require_roles("admin", "user")),
    controller: DocumentKnowladgeController = Depends(
        get_document_knowladge_controller
    ),
):
    result = await controller.delete_document_knowladge_handler(document_knowladge_id)
    return success_response(result, "Delete document knowladge is successfully")
