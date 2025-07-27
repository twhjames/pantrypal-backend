from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Tuple


class IReceiptGatewayProvider(ABC):
    """Port for interacting with the external receipt gateway."""

    @abstractmethod
    async def upload_receipt(self, url: str, payload: Dict[str, Any]) -> int:
        """Upload the receipt image and return HTTP status code."""
        raise NotImplementedError

    @abstractmethod
    async def fetch_receipt_result(
        self, url: str, params: Dict[str, Any]
    ) -> Tuple[int, Optional[Dict[str, Any]]]:
        """Retrieve receipt result and return status code with JSON if available."""
        raise NotImplementedError
