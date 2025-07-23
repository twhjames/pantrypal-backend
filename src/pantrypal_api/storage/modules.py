from injector import Binder, Module, singleton

from src.core.storage.ports.object_storage_provider import IObjectStorageProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.storage.adapters.relational_database_provider import (
    RelationalDatabaseProvider,
)
from src.pantrypal_api.storage.adapters.s3_provider import S3Provider


class StorageModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IDatabaseProvider, to=RelationalDatabaseProvider, scope=singleton)
        binder.bind(IObjectStorageProvider, to=S3Provider, scope=singleton)
