from datetime import datetime, timedelta, timezone

import pytest

from src.core.account.models import AuthTokenDomain
from src.pantrypal_api.account.accessors.auth_token_accessor import AuthTokenAccessor


@pytest.mark.asyncio
async def test_upsert_and_get_by_token(mock_relational_database_provider):
    accessor = AuthTokenAccessor(db_provider=mock_relational_database_provider)

    token_data = AuthTokenDomain(
        id=1,
        token="abc123",
        user_id=1,
        token_issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    # Insert token
    inserted_token = await accessor.upsert(token_data)
    assert inserted_token.token == "abc123"
    assert inserted_token.user_id == 1

    # Get token
    fetched_token = await accessor.get_by_token("abc123")
    assert fetched_token is not None
    assert fetched_token.token == "abc123"


@pytest.mark.asyncio
async def test_delete_by_token(mock_relational_database_provider):
    accessor = AuthTokenAccessor(db_provider=mock_relational_database_provider)

    token_data = AuthTokenDomain(
        id=2,
        token="to-be-deleted",
        user_id=2,
        token_issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    await accessor.upsert(token_data)
    await accessor.delete_by_token("to-be-deleted")

    assert await accessor.get_by_token("to-be-deleted") is None


@pytest.mark.asyncio
async def test_delete_by_user_id(mock_relational_database_provider):
    accessor = AuthTokenAccessor(db_provider=mock_relational_database_provider)

    token_data = AuthTokenDomain(
        id=3,
        token="by-user-id",
        user_id=999,
        token_issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    await accessor.upsert(token_data)
    await accessor.delete_by_user_id(999)

    assert await accessor.get_by_token("by-user-id") is None
