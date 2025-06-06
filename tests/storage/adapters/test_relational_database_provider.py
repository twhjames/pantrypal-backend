import pytest
from sqlalchemy import text

from src.core.common.constants import SecretKey
from src.pantrypal_api.storage.adapters.relational_database_provider import (
    RelationalDatabaseProvider,
)


@pytest.mark.asyncio
async def test_get_db_returns_valid_session(mock_secret_key_provider):
    # Return valid SQLite URL only when key is DATABASE_URL
    mock_secret_key_provider.get_secret.side_effect = lambda key: (
        "sqlite+aiosqlite:///:memory:" if key == SecretKey.DATABASE_URL else None
    )

    provider = RelationalDatabaseProvider(secret_provider=mock_secret_key_provider)

    async with provider.get_db() as session:
        result = await session.execute(text("SELECT 1"))
        assert result.scalar() == 1
