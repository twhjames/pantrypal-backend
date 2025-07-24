from injector import inject

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
    def __init__(self, upload_service: ObjectStorageService) -> None:
        self.upload_service = upload_service

    def create_url(self, user_id: int) -> dict:
        return self.upload_service.create_receipt_upload_url_poc(user_id)
