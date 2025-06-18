from datetime import date, timedelta

from src.core.expiry.ports.supermarket_expiry_provider import ISupermarketExpiryProvider


class FairPriceExpiryProvider(ISupermarketExpiryProvider):
    """
    Simulated adapter for FairPrice's expiry system.

    Fetches expiry based on product barcode.
    """

    async def fetch_expiry_date(self, **kwargs) -> date:
        barcode = kwargs.get("barcode")

        if not barcode:
            raise LookupError("Barcode is required to fetch expiry from FairPrice.")

        if barcode and barcode.startswith("FPD"):  # Dairy
            return date.today() + timedelta(days=8)
        elif barcode and barcode.startswith("FPS"):  # Seafood
            return date.today() + timedelta(days=3)

        raise LookupError("FairPrice expiry not available for given input.")
