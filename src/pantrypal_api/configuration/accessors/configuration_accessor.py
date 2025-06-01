from typing import Optional

from sqlalchemy import select

from src.core.configuration.accessors.configuration_accessor import (
    IConfigurationAccessor,
)
from src.core.configuration.constants import ConfigurationKey
from src.core.configuration.models import ConfigurationDomain
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.configuration.models import Configuration


class ConfigurationAccessor(IConfigurationAccessor):
    def __init__(self, db_provider: IDatabaseProvider):
        self.db_provider = db_provider

    async def get_by_key(self, key: ConfigurationKey) -> Optional[ConfigurationDomain]:
        async with self.db_provider.get_db() as session:
            stmt = select(Configuration).where(Configuration.key == key.value)
            result = await session.execute(stmt)
            config = result.scalar_one_or_none()
            return config.to_domain() if config else None
