from injector import Binder, BoundKey, Module, inject, multiprovider, singleton

from src.core.expiry.constants import SupermarketType
from src.core.expiry.ports.expiry_prediction_provider import IExpiryPredictionProvider
from src.core.expiry.ports.supermarket_expiry_provider import ISupermarketExpiryProvider
from src.pantrypal_api.expiry.adapters.fairprice_expiry_provider import (
    FairPriceExpiryProvider,
)
from src.pantrypal_api.expiry.adapters.giant_expiry_provider import GiantExpiryProvider
from src.pantrypal_api.expiry.adapters.static_expiry_provider import (
    StaticExpiryPredictionProvider,
)

# Define BoundKey tokens
FairPriceProviderKey = BoundKey(ISupermarketExpiryProvider, name="fairprice")
GiantProviderKey = BoundKey(ISupermarketExpiryProvider, name="giant")


class ExpiryModule(Module):
    def configure(self, binder: Binder) -> None:
        # Fallback expiry provider
        binder.bind(
            IExpiryPredictionProvider,
            to=StaticExpiryPredictionProvider,
            scope=singleton,
        )

        # Named bindings using BoundKey
        binder.bind(FairPriceProviderKey, to=FairPriceExpiryProvider, scope=singleton)
        binder.bind(GiantProviderKey, to=GiantExpiryProvider, scope=singleton)

    @singleton
    @multiprovider
    @inject
    def provide_supermarket_expiry_registry(
        self,
        fairprice=FairPriceProviderKey,
        giant=GiantProviderKey,
    ) -> dict[SupermarketType, ISupermarketExpiryProvider]:
        """Provides a registry mapping SupermarketType to their expiry providers."""
        return {
            SupermarketType.FAIRPRICE: fairprice,
            SupermarketType.GIANT: giant,
        }
