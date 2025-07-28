from injector import inject

from src.core.receipt.constants import ReceiptStatus
from src.core.receipt.services.receipt_gateway_service import ReceiptGatewayService
from src.core.receipt.services.receipt_service import ReceiptService
from src.core.storage.services.object_storage_service import ObjectStorageService


class ReceiptController:
    @inject
    def __init__(self, receipt_service: ReceiptService) -> None:
        self.receipt_service = receipt_service

    async def handle_receipt_webhook(self, user_id: int, receipt: dict) -> None:
        await self.receipt_service.process_receipt_webhook(user_id, receipt)


class ReceiptUploadController:
    @inject
    def __init__(
        self,
        upload_service: ObjectStorageService,
        gateway_service: ReceiptGatewayService,
    ) -> None:
        self.upload_service = upload_service
        self.gateway_service = gateway_service

    def create_url(self, user_id: int) -> dict:
        return self.upload_service.create_receipt_upload_url(user_id)

    async def upload_image(self, user_id: int, image_base64: str) -> dict | None:
        return await self.gateway_service.upload_receipt(user_id, image_base64)

    async def poll_result(self, user_id: int, receipt_id: str) -> ReceiptStatus | None:
        return await self.gateway_service.poll_receipt_result(user_id, receipt_id)
