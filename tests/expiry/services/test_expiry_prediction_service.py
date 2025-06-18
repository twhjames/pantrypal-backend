from datetime import date, timedelta

import pytest

from src.core.expiry.constants import SupermarketType
from src.core.expiry.services.expiry_prediction_service import ExpiryPredictionService
from src.core.pantry.constants import Category


@pytest.mark.asyncio
class TestExpiryPredictionService:
    async def test_uses_supermarket_provider_if_available(
        self,
        mock_expiry_prediction_provider,
        mock_supermarket_expiry_provider,
        mock_logging_provider,
    ):
        # Arrange
        mock_supermarket_expiry_provider.fetch_expiry_date.return_value = (
            date.today() + timedelta(days=2)
        )

        service = ExpiryPredictionService(
            fallback_expiry_provider=mock_expiry_prediction_provider,
            supermarket_expiry_provider={
                SupermarketType.FAIRPRICE: mock_supermarket_expiry_provider
            },
            logging_provider=mock_logging_provider,
        )

        # Act
        result = await service.get_expiry_date(
            category=Category.DAIRY,
            purchase_date=date.today(),
            supermarket_type=SupermarketType.FAIRPRICE,
            barcode="FPD1234",
        )

        # Assert
        assert isinstance(result, date)
        mock_supermarket_expiry_provider.fetch_expiry_date.assert_awaited_once()

    async def test_falls_back_to_static_if_supermarket_missing(
        self,
        mock_expiry_prediction_provider,
        mock_logging_provider,
    ):
        # Arrange
        mock_expiry_prediction_provider.predict_expiry_date.return_value = (
            date.today() + timedelta(days=10)
        )

        service = ExpiryPredictionService(
            fallback_expiry_provider=mock_expiry_prediction_provider,
            supermarket_expiry_provider={},  # empty provider registry
            logging_provider=mock_logging_provider,
        )

        # Act
        result = await service.get_expiry_date(
            category=Category.DAIRY,
            purchase_date=date.today(),
            supermarket_type=SupermarketType.FAIRPRICE,
        )

        # Assert
        assert isinstance(result, date)
        mock_expiry_prediction_provider.predict_expiry_date.assert_awaited_once()

    async def test_falls_back_to_static_on_provider_exception(
        self,
        mock_expiry_prediction_provider,
        mock_supermarket_expiry_provider,
        mock_logging_provider,
    ):
        # Arrange
        mock_supermarket_expiry_provider.fetch_expiry_date.side_effect = Exception(
            "API error"
        )
        mock_expiry_prediction_provider.predict_expiry_date.return_value = (
            date.today() + timedelta(days=5)
        )

        service = ExpiryPredictionService(
            fallback_expiry_provider=mock_expiry_prediction_provider,
            supermarket_expiry_provider={
                SupermarketType.FAIRPRICE: mock_supermarket_expiry_provider
            },
            logging_provider=mock_logging_provider,
        )

        # Act
        result = await service.get_expiry_date(
            category=Category.DAIRY,
            purchase_date=date.today(),
            supermarket_type=SupermarketType.FAIRPRICE,
        )

        # Assert
        assert isinstance(result, date)
        mock_expiry_prediction_provider.predict_expiry_date.assert_awaited_once()
        mock_supermarket_expiry_provider.fetch_expiry_date.assert_awaited_once()
