from typing import Any, Dict, Optional
from uuid import uuid4

from injector import inject

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.receipt.accessors.receipt_result_accessor import IReceiptResultAccessor
from src.core.receipt.constants import ReceiptStatus
from src.core.receipt.models import ReceiptResultDomain
from src.core.receipt.ports.receipt_gateway_provider import IReceiptGatewayProvider
from src.core.receipt.services.receipt_service import ReceiptService


class ReceiptGatewayService:
    """Interact with the AWS API Gateway for receipt processing."""

    @inject
    def __init__(
        self,
        secret_provider: ISecretProvider,
        logging_provider: ILoggingProvider,
        receipt_service: ReceiptService,
        gateway_provider: IReceiptGatewayProvider,
        receipt_result_accessor: IReceiptResultAccessor,
    ) -> None:
        self.secret_provider = secret_provider
        self.logging_provider = logging_provider
        self.receipt_service = receipt_service
        self.gateway_provider = gateway_provider
        self.receipt_result_accessor = receipt_result_accessor

    # TODO: Prevent same receipt upload (both image file and image's content)
    async def upload_receipt(
        self, user_id: int, image_base64: str
    ) -> Optional[Dict[str, Any]]:
        url = self.secret_provider.get_secret(SecretKey.RECEIPT_UPLOAD_ENDPOINT)
        if not url:
            self.logging_provider.error(
                "RECEIPT_UPLOAD_ENDPOINT is not configured",
                tag="ReceiptGatewayService",
            )
            return None

        receipt_id = f"{uuid4()}.jpg"
        payload = {
            "user_id": str(user_id),
            "receipt_id": receipt_id,
            "image_base64": image_base64,
        }
        try:
            status = await self.gateway_provider.upload_receipt(url, payload)
        except Exception as exc:  # pragma: no cover - network
            self.logging_provider.error(
                "Failed to upload receipt",
                extra_data={"error": str(exc)},
                tag="ReceiptGatewayService",
            )
            return None

        if 200 <= status < 300:
            return {"receipt_id": receipt_id}

        self.logging_provider.error(
            "Unexpected status from receipt upload",
            extra_data={"status": status},
            tag="ReceiptGatewayService",
        )
        return None

    async def poll_receipt_result(
        self, user_id: int, receipt_id: str
    ) -> Optional[ReceiptStatus]:
        existing = await self.receipt_result_accessor.get_result(user_id, receipt_id)
        if existing:
            return ReceiptStatus.PROCESSED
        url = self.secret_provider.get_secret(SecretKey.RECEIPT_RETRIEVE_ENDPOINT)
        if not url:
            self.logging_provider.error(
                "RECEIPT_RETRIEVE_ENDPOINT is not configured",
                tag="ReceiptGatewayService",
            )
            return None
        params = {"user_id": str(user_id), "receipt_id": receipt_id}
        try:
            status, result = await self.gateway_provider.fetch_receipt_result(
                url, params
            )
        except Exception as exc:  # pragma: no cover - network
            self.logging_provider.error(
                "Failed to poll receipt result",
                extra_data={"error": str(exc)},
                tag="ReceiptGatewayService",
            )
            return None

        if status == 200 and result is not None:
            domain = ReceiptResultDomain.create(
                user_id=user_id, receipt_id=receipt_id, result=result
            )
            await self.receipt_result_accessor.add_result(domain)
            await self.receipt_service.process_receipt_webhook(user_id, result)
            return ReceiptStatus.PROCESSED
        if status == 202:
            return ReceiptStatus.PENDING
        self.logging_provider.error(
            "Unexpected status from receipt result",
            extra_data={"status": status},
            tag="ReceiptGatewayService",
        )
        return None
