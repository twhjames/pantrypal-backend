from datetime import date, timedelta

from src.core.expiry.ports.supermarket_expiry_provider import ISupermarketExpiryProvider


class GiantExpiryProvider(ISupermarketExpiryProvider):
    """
    Simulated adapter for Giant's expiry system.

    Fetches expiry date based on product barcode.
    """

    async def fetch_expiry_date(self, **kwargs) -> date:
        barcode = kwargs.get("barcode")

        if not barcode:
            raise LookupError("Barcode is required to fetch expiry from Giant.")

        if barcode.startswith("GNTM"):  # Meat
            return date.today() + timedelta(days=4)
        elif barcode.startswith("GNTV"):  # Vegetables
            return date.today() + timedelta(days=5)

        raise LookupError("Giant expiry not available for given barcode.")
