from typing import Optional

from injector import inject

from src.core.common.constants import JSON_FIELD_OPTION_TYPES
from src.core.configuration.accessors.configuration_accessor import (
    IConfigurationAccessor,
)
from src.core.configuration.constants import ConfigurationDefault, ConfigurationKey
from src.core.configuration.models import ConfigurationDomain


class ConfigurationService:
    @inject
    def __init__(self, configuration_accessor: IConfigurationAccessor):
        self.configuration_accessor = configuration_accessor

    def get_notification_email_sender_name(self) -> str:
        configuration_domain = self.configuration_accessor.get_by_key(
            ConfigurationKey.NOTIFICATION_EMAIL_SENDER_NAME
        )

        value = (
            self._get_configuration_value(configuration_domain)
            or ConfigurationDefault.NOTIFICATION_EMAIL_SENDER_NAME.value
        )

        return value

    def get_notification_email_sender(self) -> int:
        configuration_domain = self.configuration_accessor.get_by_key(
            ConfigurationKey.NOTIFICATION_EMAIL_SENDER
        )

        value = int(
            self._get_configuration_value(configuration_domain)
            or ConfigurationDefault.NOTIFICATION_EMAIL_SENDER.value
        )

        return value

    @staticmethod
    def _get_configuration_value(
        configuration_domain: Optional[ConfigurationDomain],
    ) -> JSON_FIELD_OPTION_TYPES:
        if not configuration_domain:
            return {}

        return configuration_domain.value
