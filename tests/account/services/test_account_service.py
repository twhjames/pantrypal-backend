import pytest

from src.core.account.models import UserAccountDomain
from src.core.account.services.user_account_service import UserAccountService
from src.core.account.specs import RegisterUserSpec, UpdateUserSpec


@pytest.mark.asyncio
async def test_register_user_success(
    mock_user_account_accessor, mock_auth_provider, mock_logging_provider
):
    mock_user_account_accessor.get_by_email.return_value = None
    mock_auth_provider.get_hashed_password.return_value = "securehash"

    created_user = UserAccountDomain(
        id=1, username="newuser", email="a@x.com", password_hash="securehash"
    )
    mock_user_account_accessor.create_user.return_value = created_user

    service = UserAccountService(
        mock_user_account_accessor,
        mock_auth_provider,
        None,
        mock_logging_provider,
    )

    spec = RegisterUserSpec(username="newuser", email="a@x.com", password="securepw")
    user = await service.register_user(spec)

    assert user.username == "newuser"
    assert user.email == "a@x.com"


@pytest.mark.asyncio
async def test_update_user(
    mock_user_account_accessor, mock_auth_provider, mock_logging_provider
):
    user_before = UserAccountDomain(
        id=1, username="before", email="b@x.com", password_hash="old"
    )
    user_after = UserAccountDomain(
        id=1, username="after", email="a@x.com", password_hash="newhash"
    )

    mock_user_account_accessor.get_by_id.return_value = user_before
    mock_auth_provider.get_hashed_password.return_value = "newhash"
    mock_user_account_accessor.update_user.return_value = user_after

    service = UserAccountService(
        mock_user_account_accessor,
        mock_auth_provider,
        None,
        mock_logging_provider,
    )
    spec = UpdateUserSpec(username="after", email="a@x.com", password="newpassword")
    user = await service.update_user(1, spec)

    assert user.username == "after"
    assert user.password_hash == "newhash"


@pytest.mark.asyncio
async def test_delete_user(
    mock_user_account_accessor, mock_auth_token_accessor, mock_logging_provider
):
    user = UserAccountDomain(
        id=1, username="delete", email="d@x.com", password_hash="x"
    )
    mock_user_account_accessor.get_by_id.return_value = user

    service = UserAccountService(
        mock_user_account_accessor,
        None,
        mock_auth_token_accessor,
        mock_logging_provider,
    )
    await service.delete_user(1)

    mock_auth_token_accessor.delete_by_user_id.assert_called_once_with(1)
    mock_user_account_accessor.delete_by_id.assert_called_once_with(1)
