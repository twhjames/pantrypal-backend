from typing import Any, Dict, Optional, Tuple

import httpx
from injector import inject

from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.receipt.ports.receipt_gateway_provider import IReceiptGatewayProvider


class HttpReceiptGatewayProvider(IReceiptGatewayProvider):
    """HTTP implementation for the receipt gateway."""

    @inject
    def __init__(self, logging_provider: ILoggingProvider) -> None:
        self.logging_provider = logging_provider

    async def upload_receipt(self, url: str, payload: Dict[str, Any]) -> int:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(url, json=payload)
                return resp.status_code
            except Exception as exc:  # pragma: no cover - network
                self.logging_provider.error(
                    "Failed to upload receipt",
                    extra_data={"error": str(exc)},
                    tag="HttpReceiptGatewayProvider",
                )
                raise

    async def fetch_receipt_result(
        self, url: str, params: Dict[str, Any]
    ) -> Tuple[int, Optional[Dict[str, Any]]]:
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params)
            except Exception as exc:  # pragma: no cover - network
                self.logging_provider.error(
                    "Failed to fetch receipt result",
                    extra_data={"error": str(exc)},
                    tag="HttpReceiptGatewayProvider",
                )
                raise
        data: Optional[Dict[str, Any]] = None
        if resp.status_code == 200:
            try:
                data = resp.json()
            except Exception as exc:  # pragma: no cover - invalid json
                self.logging_provider.error(
                    "Invalid JSON from receipt result",
                    extra_data={"error": str(exc)},
                    tag="HttpReceiptGatewayProvider",
                )
                raise
        return resp.status_code, data
