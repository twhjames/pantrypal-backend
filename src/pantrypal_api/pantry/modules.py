from injector import Binder, Module, singleton

from src.core.pantry.accessors.pantry_item_accessor import IPantryItemAccessor
from src.pantrypal_api.pantry.accessors.pantry_item_accessor import PantryItemAccessor


class PantryModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IPantryItemAccessor, to=PantryItemAccessor, scope=singleton)
