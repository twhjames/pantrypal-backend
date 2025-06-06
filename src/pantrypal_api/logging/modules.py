from injector import Binder, Module, singleton

from src.core.logging.ports.logging_provider import ILoggingProvider
from src.pantrypal_api.logging.adapters.logging_provider import AppLoggingProvider


class LoggingModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ILoggingProvider, to=AppLoggingProvider, scope=singleton)
