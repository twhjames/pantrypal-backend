from abc import ABC, abstractmethod
from typing import Optional

from src.core.receipt.models import ReceiptResultDomain


class IReceiptResultAccessor(ABC):
    """Accessor for storing processed receipt results."""

    @abstractmethod
    async def get_result(
        self, user_id: int, receipt_id: str
    ) -> Optional[ReceiptResultDomain]:
        """Return result if it exists."""
        raise NotImplementedError

    @abstractmethod
    async def add_result(self, result: ReceiptResultDomain) -> ReceiptResultDomain:
        """Persist a new receipt result."""
        raise NotImplementedError
