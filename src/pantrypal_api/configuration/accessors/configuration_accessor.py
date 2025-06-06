from typing import Optional

from sqlalchemy import select

from src.core.configuration.accessors.configuration_accessor import (
    IConfigurationAccessor,
)
from src.core.configuration.constants import ConfigurationKey
from src.core.configuration.models import ConfigurationDomain
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.configuration.models import Configuration


class ConfigurationAccessor(IConfigurationAccessor):
    def __init__(
        self, db_provider: IDatabaseProvider, logging_provider: ILoggingProvider
    ):
        self.db_provider = db_provider
        self.logging_provider = logging_provider

    async def get_by_key(self, key: ConfigurationKey) -> Optional[ConfigurationDomain]:
        async with self.db_provider.get_db() as session:
            stmt = select(Configuration).where(Configuration.key == key.value)
            result = await session.execute(stmt)
            config = result.scalar_one_or_none()

            if not config:
                self.logging_provider.warning(
                    f"Configuration key not found: {key.value}", tag="Configuration"
                )

            return config.to_domain() if config else None
