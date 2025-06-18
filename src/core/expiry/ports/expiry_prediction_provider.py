from abc import ABC, abstractmethod
from datetime import date

from src.core.pantry.constants import Category


class IExpiryPredictionProvider(ABC):
    """Port interface for predicting expiry date based on category and purchase date."""

    @abstractmethod
    async def predict_expiry_date(
        self, category: Category, purchase_date: date
    ) -> date:
        """Predict expiry date given a category and purchase date."""
        raise NotImplementedError
