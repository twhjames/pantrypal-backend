from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response

from src.core.receipt.constants import ReceiptStatus
from src.core.receipt.services.receipt_gateway_service import ReceiptGatewayService
from src.core.receipt.services.receipt_service import ReceiptService
from src.core.storage.services.object_storage_service import ObjectStorageService
from src.pantrypal_api.account.dependencies import get_current_user
from src.pantrypal_api.modules import injector
from src.pantrypal_api.receipt.controllers.receipt_controller import (
    ReceiptController,
    ReceiptUploadController,
)
from src.pantrypal_api.receipt.schemas.receipt_schemas import (
    ReceiptUploadRequest,
    ReceiptWebhookRequest,
)

router = APIRouter(prefix="/receipt", tags=["Receipt"])


def get_receipt_controller() -> ReceiptController:
    service = injector.get(ReceiptService)
    return ReceiptController(service)


def get_upload_controller() -> ReceiptUploadController:
    storage_service = injector.get(ObjectStorageService)
    gateway_service = injector.get(ReceiptGatewayService)
    return ReceiptUploadController(storage_service, gateway_service)


@router.post("/webhook", status_code=status.HTTP_204_NO_CONTENT)
async def receipt_webhook(
    request: ReceiptWebhookRequest,
    controller: ReceiptController = Depends(get_receipt_controller),
):
    await controller.handle_receipt_webhook(request.user_id, request.receipt)


@router.post("/presigned-url")
async def create_presigned_url(
    controller: ReceiptUploadController = Depends(get_upload_controller),
    current_user_id: int = Depends(get_current_user),
):
    return controller.create_url(current_user_id)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_receipt(
    request: ReceiptUploadRequest,
    controller: ReceiptUploadController = Depends(get_upload_controller),
    current_user_id: int = Depends(get_current_user),
):
    result = await controller.upload_image(current_user_id, request.image_base64)
    if result is None:
        raise HTTPException(status_code=500, detail="Failed to upload receipt")
    return result


@router.get("/result/{receipt_id}")
async def get_receipt_result(
    receipt_id: str,
    controller: ReceiptUploadController = Depends(get_upload_controller),
    current_user_id: int = Depends(get_current_user),
):
    status_value = await controller.poll_result(current_user_id, receipt_id)
    if status_value is None:
        raise HTTPException(status_code=500, detail="Failed to poll receipt")
    if status_value == ReceiptStatus.PROCESSED:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    if status_value == ReceiptStatus.PENDING:
        return JSONResponse(
            {"status": ReceiptStatus.PENDING}, status_code=status.HTTP_202_ACCEPTED
        )
    raise HTTPException(status_code=500, detail="Unexpected receipt status")
