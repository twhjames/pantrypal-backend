from datetime import datetime, timedelta, timezone

import pytest

from src.core.account.models import AuthTokenDomain, UserAccountDomain
from src.core.account.services.auth_service import AuthService
from src.core.account.specs import LoginSpec


@pytest.mark.asyncio
async def test_login_success(
    mock_auth_provider,
    mock_user_account_accessor,
    mock_auth_token_accessor,
    mock_logging_provider,
):
    user = UserAccountDomain(
        id=1,
        username="test",
        email="test@example.com",
        password_hash="pass_hashed",
        is_admin=False,
    )
    token = AuthTokenDomain(
        id=1,
        token="mock-token",
        user_id=1,
        token_issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )

    mock_user_account_accessor.get_by_email.return_value = user
    mock_auth_provider.verify_password.return_value = True
    mock_auth_provider.generate_token.return_value = "mock-token"
    mock_auth_token_accessor.upsert.return_value = token

    service = AuthService(
        mock_auth_provider,
        mock_user_account_accessor,
        mock_auth_token_accessor,
        mock_logging_provider,
    )
    result = await service.login(LoginSpec(email="test@example.com", password="pass"))

    assert result.token == "mock-token"
    assert result.user_id == 1


@pytest.mark.asyncio
async def test_logout_success(mock_auth_token_accessor, mock_logging_provider):
    token = AuthTokenDomain(
        id=1,
        token="abc",
        user_id=1,
        token_issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    mock_auth_token_accessor.get_by_token.return_value = token

    service = AuthService(None, None, mock_auth_token_accessor, mock_logging_provider)
    await service.logout("abc")

    mock_auth_token_accessor.delete_by_token.assert_called_once_with("abc")
