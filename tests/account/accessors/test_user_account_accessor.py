import pytest

from src.core.account.models import UserAccountDomain
from src.pantrypal_api.account.accessors.user_account_accessor import (
    UserAccountAccessor,
)


@pytest.mark.asyncio
async def test_create_and_get_user(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = UserAccountAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    user = UserAccountDomain(
        id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hashedpass",
        is_admin=False,
    )

    created = await accessor.create_user(user)
    assert created.id is not None
    assert created.email == "test@example.com"

    by_id = await accessor.get_by_id(created.id)
    assert by_id is not None
    assert by_id.username == "testuser"

    by_email = await accessor.get_by_email("test@example.com")
    assert by_email is not None
    assert by_email.id == created.id


@pytest.mark.asyncio
async def test_update_user(mock_relational_database_provider, mock_logging_provider):
    accessor = UserAccountAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    user = UserAccountDomain(
        id=2,
        username="before",
        email="update@example.com",
        password_hash="pass",
        is_admin=False,
    )
    created = await accessor.create_user(user)

    updated = UserAccountDomain(
        id=created.id,
        username="after",
        email="update@example.com",
        password_hash="newpass",
        is_admin=False,
    )

    result = await accessor.update_user(updated)
    assert result.username == "after"
    assert result.password_hash == "newpass"


@pytest.mark.asyncio
async def test_delete_user(mock_relational_database_provider, mock_logging_provider):
    accessor = UserAccountAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    user = UserAccountDomain(
        id=3,
        username="todelete",
        email="delete@example.com",
        password_hash="deletehash",
        is_admin=False,
    )
    created = await accessor.create_user(user)

    await accessor.delete_by_id(created.id)
    assert await accessor.get_by_id(created.id) is None
