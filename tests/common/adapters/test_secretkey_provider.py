from src.core.common.constants import SecretKey
from src.pantrypal_api.common.adapters.secretkey_provider import (
    EnvVariableSecretProvider,
)


def test_env_variable_secret_provider(monkeypatch):
    """Should return value from env when key exists."""
    monkeypatch.setenv("TEST_KEY", "super-secret")

    class DummySecretKey:
        name = "TEST_KEY"

    provider = EnvVariableSecretProvider()
    result = provider.get_secret(DummySecretKey())
    assert result == "super-secret"


def test_env_variable_secret_provider_default(monkeypatch):
    """Should return fallback if key is missing."""
    monkeypatch.delenv("MISSING_KEY", raising=False)

    class DummySecretKey:
        name = "MISSING_KEY"

    provider = EnvVariableSecretProvider()
    result = provider.get_secret(DummySecretKey(), default="fallback")
    assert result == "fallback"


def test_env_variable_secret_provider_real_key(monkeypatch):
    """Should return value using real SecretKey enum."""
    monkeypatch.setenv("AUTH_ALGORITHM", "mock-auth-algo")

    provider = EnvVariableSecretProvider()
    result = provider.get_secret(SecretKey.AUTH_ALGORITHM)
    assert result == "mock-auth-algo"
