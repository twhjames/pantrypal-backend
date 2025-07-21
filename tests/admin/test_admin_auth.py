import pytest

try:
    from src.pantrypal_api.admin.auth import AdminAuth
except ModuleNotFoundError:
    AdminAuth = None


@pytest.mark.asyncio
async def test_admin_auth_uses_secret_provider(mock_secret_key_provider):
    if AdminAuth is None:
        pytest.skip("sqladmin not installed")
    mock_secret_key_provider.get_secret.return_value = "sek"
    backend = AdminAuth(secret_provider=mock_secret_key_provider)
    assert getattr(backend, "secret_key", None) == "sek"
