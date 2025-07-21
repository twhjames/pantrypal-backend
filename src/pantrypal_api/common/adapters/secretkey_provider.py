import os
from typing import Optional

from dotenv import load_dotenv
from injector import inject

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider


class EnvVariableSecretProvider(ISecretProvider):
    @inject
    def __init__(self, logging_provider: ILoggingProvider):
        self.logging_provider = logging_provider
        # Load environment variables from a .env file if present
        load_dotenv()

    def get_secret(
        self, key: SecretKey, default: Optional[str] = None
    ) -> Optional[str]:
        value = os.getenv(key.name, default)
        if value is None and self.logging_provider:
            self.logging_provider.warning(
                f"Missing environment variable for key: {key.name}", tag="Secrets"
            )
        elif default is not None and self.logging_provider:
            self.logging_provider.info(
                f"Using default value for missing key: {key.name}",
                extra_data={"default": default},
                tag="Secrets",
            )
        return value
