from injector import Binder, Module, singleton

from src.core.configuration.accessors.configuration_accessor import (
    IConfigurationAccessor,
)
from src.pantrypal_api.configuration.accessors.configuration_accessor import (
    ConfigurationAccessor,
)


class ConfigurationModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IConfigurationAccessor, to=ConfigurationAccessor, scope=singleton)
