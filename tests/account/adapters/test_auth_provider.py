import pytest
from jose import jwt

from src.core.account.ports.auth_provider import IAuthProvider
from src.core.common.constants import SecretKey
from src.pantrypal_api.account.adapters.auth_provider import AuthProvider

# === Fixture: Secret Key Provider with Auth Settings ===


@pytest.fixture
def mock_secret_key_provider_with_auth_secrets():
    """
    Provides a mock implementation of ISecretKeyProvider with valid secrets.
    Used for initializing AuthProvider in a controlled test environment.
    """

    class CustomSecretKeyProvider:
        def get_secret(self, key):
            return {
                SecretKey.AUTH_SECRET_KEY: "test-secret-key",
                SecretKey.AUTH_ALGORITHM: "HS256",
                SecretKey.AUTH_TOKEN_EXPIRY_MINUTES: "60",
            }.get(key)

    return CustomSecretKeyProvider()


# === Test: Password Hashing & Verification ===


def test_get_hashed_password_and_verify(mock_secret_key_provider_with_auth_secrets):
    provider: IAuthProvider = AuthProvider(
        secret_provider=mock_secret_key_provider_with_auth_secrets
    )

    raw_password = "my_password"
    hashed = provider.get_hashed_password(raw_password)

    assert hashed != raw_password, "Hashed password should not match raw input"
    assert provider.verify_password(raw_password, hashed) is True
    assert provider.verify_password("wrong_password", hashed) is False


# === Test: Valid JWT Token Generation ===


def test_generate_token_valid_jwt(mock_secret_key_provider_with_auth_secrets):
    provider: IAuthProvider = AuthProvider(
        secret_provider=mock_secret_key_provider_with_auth_secrets
    )

    user_id = 123
    token = provider.generate_token(user_id)

    decoded = jwt.decode(token, "test-secret-key", algorithms=["HS256"])

    assert decoded["sub"] == str(user_id)
    assert "exp" in decoded


# === Test: Missing Secret Key Should Raise Error ===


def test_invalid_secret_key_raises():
    class IncompleteSecretKeyProvider:
        def get_secret(self, key):
            return None  # Simulate missing secrets

    provider = AuthProvider(secret_provider=IncompleteSecretKeyProvider())

    with pytest.raises(ValueError, match="AUTH_SECRET_KEY is missing"):
        provider.generate_token(user_id=1)


# === Test: Invalid Expiry Format Should Raise Error ===


def test_invalid_expiry_minutes_raises():
    class InvalidExpiryProvider:
        def get_secret(self, key):
            return {
                SecretKey.AUTH_SECRET_KEY: "secret",
                SecretKey.AUTH_ALGORITHM: "HS256",
                SecretKey.AUTH_TOKEN_EXPIRY_MINUTES: "invalid",  # Not an integer
            }.get(key)

    provider = AuthProvider(secret_provider=InvalidExpiryProvider())

    with pytest.raises(ValueError, match="Invalid AUTH_TOKEN_EXPIRY_MINUTES"):
        provider.generate_token(user_id=1)
