from abc import ABC, abstractmethod
from datetime import date


class ISupermarketExpiryProvider(ABC):
    """Port interface for fetching expiry information from partnered supermarket systems."""

    @abstractmethod
    async def fetch_expiry_date(self, **kwargs) -> date:
        """
        Fetch expiry date from a partnered supermarket system.

        Accepts flexible keyword arguments (e.g., transaction ID, barcode)
        depending on the specific supermarket integration.
        """
        raise NotImplementedError
