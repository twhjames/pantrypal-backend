from typing import Optional

from injector import inject

from src.core.configuration.accessors.configuration_accessor import (
    IConfigurationAccessor,
)
from src.core.configuration.constants import ConfigurationDefault, ConfigurationKey
from src.core.configuration.models import ConfigurationDomain


class ConfigurationService:
    @inject
    def __init__(self, configuration_accessor: IConfigurationAccessor):
        self.configuration_accessor = configuration_accessor

    async def get_notification_email_sender_name(self) -> str:
        configuration_domain = await self.configuration_accessor.get_by_key(
            ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME
        )

        value = (
            self._get_configuration_value(configuration_domain)
            or ConfigurationDefault.NOTIFICATION_EMAIL_SENDER_NAME.value
        )

        return value

    async def get_notification_email_sender(self) -> str:
        configuration_domain = await self.configuration_accessor.get_by_key(
            ConfigurationKey.NOTIFICATION_EMAIL_SENDER
        )

        value = (
            self._get_configuration_value(configuration_domain)
            or ConfigurationDefault.NOTIFICATION_EMAIL_SENDER.value
        )

        return value

    @staticmethod
    def _get_configuration_value(
        configuration_domain: Optional[ConfigurationDomain],
    ) -> Optional[str]:
        if not configuration_domain:
            return None
        return configuration_domain.value
