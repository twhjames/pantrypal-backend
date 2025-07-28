from datetime import date

from injector import inject

from src.core.expiry.constants import SupermarketType
from src.core.expiry.ports.expiry_prediction_provider import IExpiryPredictionProvider
from src.core.expiry.ports.supermarket_expiry_provider import ISupermarketExpiryProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.pantry.constants import Category


class ExpiryPredictionService:
    """
    Service that attempts to fetch expiry data from a partnered supermarket provider
    based on supermarket type, and falls back to static prediction if unavailable.
    """

    @inject
    def __init__(
        self,
        fallback_expiry_provider: IExpiryPredictionProvider,
        supermarket_expiry_provider: dict[SupermarketType, ISupermarketExpiryProvider],
        logging_provider: ILoggingProvider,
    ):
        self.fallback_expiry_provider = fallback_expiry_provider
        self.supermarket_expiry_provider = supermarket_expiry_provider
        self.logging_provider = logging_provider

    async def get_expiry_date(
        self,
        category: Category,
        purchase_date: date,
        supermarket_type: SupermarketType | None = None,
        **kwargs,
    ) -> date:
        if supermarket_type:
            provider = self.supermarket_expiry_provider.get(supermarket_type)
            if provider:
                try:
                    expiry_date = await provider.fetch_expiry_date(
                        category=category, purchase_date=purchase_date, **kwargs
                    )
                    self.logging_provider.info(
                        "Fetched expiry from supermarket provider",
                        tag="ExpiryService",
                        extra_data={
                            "supermarket_type": supermarket_type.value,
                            "expiry_date": str(expiry_date),
                        },
                    )
                    return expiry_date
                except Exception as e:
                    self.logging_provider.warning(
                        "Supermarket provider failed, falling back to static prediction",
                        tag="ExpiryService",
                        extra_data={
                            "supermarket_type": supermarket_type.value,
                            "error": str(e),
                        },
                    )
            else:
                self.logging_provider.debug(
                    "No provider found for given supermarket_type, falling back",
                    tag="ExpiryService",
                    extra_data={"supermarket_type": supermarket_type.value},
                )

        fallback_date = await self.fallback_expiry_provider.predict_expiry_date(
            category, purchase_date
        )
        self.logging_provider.info(
            "Used fallback static expiry prediction",
            tag="ExpiryService",
            extra_data={
                "category": category.value,
                "purchase_date": str(purchase_date),
                "predicted_expiry": str(fallback_date),
            },
        )
        return fallback_date
