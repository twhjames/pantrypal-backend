import pytest

from src.core.common.constants import SecretKey
from src.pantrypal_api.common.adapters.secretkey_provider import (
    EnvVariableSecretProvider,
)


# Real EnvVariableSecretProvider with mock logging
@pytest.fixture
def env_secretkey_provider(mock_logging_provider):
    return EnvVariableSecretProvider(logging_provider=mock_logging_provider)


def test_env_variable_secret_provider(monkeypatch, env_secretkey_provider):
    monkeypatch.setenv("TEST_KEY", "super-secret")

    class DummySecretKey:
        name = "TEST_KEY"

    result = env_secretkey_provider.get_secret(DummySecretKey())
    assert result == "super-secret"


def test_env_variable_secret_provider_default(monkeypatch, env_secretkey_provider):
    monkeypatch.delenv("MISSING_KEY", raising=False)

    class DummySecretKey:
        name = "MISSING_KEY"

    result = env_secretkey_provider.get_secret(DummySecretKey(), default="fallback")
    assert result == "fallback"


def test_env_variable_secret_provider_real_key(monkeypatch, env_secretkey_provider):
    monkeypatch.setenv("AUTH_ALGORITHM", "mock-auth-algo")
    result = env_secretkey_provider.get_secret(SecretKey.AUTH_ALGORITHM)
    assert result == "mock-auth-algo"
