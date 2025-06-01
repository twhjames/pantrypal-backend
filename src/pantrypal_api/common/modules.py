from injector import Binder, Module, singleton

from src.core.common.ports.secretkey_provider import ISecretProvider
from src.pantrypal_api.common.adapters.secretkey_provider import (
    EnvVariableSecretProvider,
)


class CommonModule(Module):
    def configure(self, binder: Binder):
        binder.bind(ISecretProvider, to=EnvVariableSecretProvider, scope=singleton)
