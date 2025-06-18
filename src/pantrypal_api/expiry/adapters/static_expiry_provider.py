from datetime import date

from src.core.expiry.constants import CATEGORY_EXPIRY_DAYS
from src.core.expiry.ports.expiry_prediction_provider import IExpiryPredictionProvider
from src.core.pantry.constants import Category


class StaticExpiryPredictionProvider(IExpiryPredictionProvider):
    """Static implementation of expiry prediction using hardcoded shelf life per category."""

    async def predict_expiry_date(
        self, category: Category, purchase_date: date
    ) -> date:
        shelf_life = CATEGORY_EXPIRY_DAYS.get(
            category, CATEGORY_EXPIRY_DAYS[Category.OTHER]
        )
        return purchase_date + shelf_life
