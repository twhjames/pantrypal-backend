from abc import ABC, abstractmethod

from src.core.configuration.constants import ConfigurationKey
from src.core.configuration.models import ConfigurationDomain


class IConfigurationAccessor(ABC):
    @abstractmethod
    async def get_by_key(self, key: ConfigurationKey) -> ConfigurationDomain:
        raise NotImplementedError
