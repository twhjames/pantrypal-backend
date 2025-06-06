import pytest
from sqlalchemy import text

from src.core.common.constants import SecretKey
from src.pantrypal_api.storage.adapters.relational_database_provider import (
    RelationalDatabaseProvider,
)


@pytest.fixture
def sqlite_relational_database_provider(
    mock_secret_key_provider, mock_logging_provider
):
    mock_secret_key_provider.get_secret.side_effect = lambda key: (
        "sqlite+aiosqlite:///:memory:" if key == SecretKey.DATABASE_URL else None
    )

    return RelationalDatabaseProvider(
        secret_provider=mock_secret_key_provider,
        logging_provider=mock_logging_provider,
    )


@pytest.mark.asyncio
async def test_get_db_returns_valid_session(sqlite_relational_database_provider):
    async with sqlite_relational_database_provider.get_db() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
