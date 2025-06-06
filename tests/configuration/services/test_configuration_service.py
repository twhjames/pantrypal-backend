from datetime import datetime, timezone

import pytest

from src.core.configuration.constants import ConfigurationDefault, ConfigurationKey
from src.core.configuration.models import ConfigurationDomain
from src.core.configuration.services.configuration_service import ConfigurationService


@pytest.mark.asyncio
async def test_get_notification_email_sender_name_returns_value(
    mock_configuration_accessor,
):
    mock_configuration_accessor.get_by_key.return_value = ConfigurationDomain(
        id=1,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
        key=ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME.value,
        value="Custom Name",
        description="desc",
    )

    service = ConfigurationService(configuration_accessor=mock_configuration_accessor)
    result = await service.get_notification_email_sender_name()
    assert result == "Custom Name"


@pytest.mark.asyncio
async def test_get_notification_email_sender_name_returns_default(
    mock_configuration_accessor,
):
    mock_configuration_accessor.get_by_key.return_value = None

    service = ConfigurationService(configuration_accessor=mock_configuration_accessor)
    result = await service.get_notification_email_sender_name()
    assert result == ConfigurationDefault.NOTIFICATION_EMAIL_SENDER_NAME.value


@pytest.mark.asyncio
async def test_get_notification_email_sender_returns_value(mock_configuration_accessor):
    mock_configuration_accessor.get_by_key.return_value = ConfigurationDomain(
        id=2,
        created_at=datetime.now(timezone.utc),
        updated_at=None,
        key=ConfigurationKey.NOTIFICATION_EMAIL_SENDER.value,
        value="support@pantrypal.ai",
        description="desc",
    )

    service = ConfigurationService(configuration_accessor=mock_configuration_accessor)
    result = await service.get_notification_email_sender()
    assert result == "support@pantrypal.ai"


@pytest.mark.asyncio
async def test_get_notification_email_sender_returns_default(
    mock_configuration_accessor,
):
    mock_configuration_accessor.get_by_key.return_value = None

    service = ConfigurationService(configuration_accessor=mock_configuration_accessor)
    result = await service.get_notification_email_sender()
    assert result == ConfigurationDefault.NOTIFICATION_EMAIL_SENDER.value
