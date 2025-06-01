import os
from typing import Optional

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider


class EnvVariableSecretProvider(ISecretProvider):
    def get_secret(
        self, key: SecretKey, default: Optional[str] = None
    ) -> Optional[str]:
        return os.getenv(key.name, default)
