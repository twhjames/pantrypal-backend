from fastapi import APIRouter, Depends, status

from src.core.receipt.services.receipt_service import ReceiptService
from src.core.storage.services.object_storage_service import ObjectStorageService
from src.pantrypal_api.account.dependencies import get_current_user
from src.pantrypal_api.modules import injector
from src.pantrypal_api.receipt.controllers.receipt_controller import (
    ReceiptController,
    ReceiptUploadController,
)
from src.pantrypal_api.receipt.schemas.receipt_schemas import ReceiptWebhookRequest

router = APIRouter(prefix="/receipt", tags=["Receipt"])


def get_receipt_controller() -> ReceiptController:
    service = injector.get(ReceiptService)
    return ReceiptController(service)


def get_upload_controller() -> ReceiptUploadController:
    service = injector.get(ObjectStorageService)
    return ReceiptUploadController(service)


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
