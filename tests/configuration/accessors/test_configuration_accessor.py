import pytest
from sqlalchemy import insert

from src.core.configuration.constants import ConfigurationKey
from src.pantrypal_api.configuration.accessors.configuration_accessor import (
    ConfigurationAccessor,
)
from src.pantrypal_api.configuration.models import Configuration


@pytest.mark.asyncio
async def test_get_by_key_returns_config(
    mock_relational_database_provider, db_session, mock_logging_provider
):
    """
    Test that ConfigurationAccessor returns the correct configuration domain when the key exists.
    """
    await db_session.execute(
        insert(Configuration).values(
            key=ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME.value,
            value="PantryPal Bot",
            description="Sender name for outgoing emails",
        )
    )
    await db_session.commit()

    accessor = ConfigurationAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    result = await accessor.get_by_key(ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME)

    assert result is not None
    assert result.key == ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME.value
    assert result.value == "PantryPal Bot"
    assert result.description == "Sender name for outgoing emails"


@pytest.mark.asyncio
async def test_get_by_key_returns_none_if_not_found(
    mock_relational_database_provider, mock_logging_provider
):
    """
    Test that ConfigurationAccessor returns None when the key does not exist.
    """
    accessor = ConfigurationAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )
    result = await accessor.get_by_key(ConfigurationKey.NOTIFICATION_EMAIL_SENDER)
    assert result is None
