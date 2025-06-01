from injector import Binder, Module, singleton

from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.storage.adapters.relational_database_provider import (
    RelationalDatabaseProvider,
)


class StorageModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IDatabaseProvider, to=RelationalDatabaseProvider, scope=singleton)
