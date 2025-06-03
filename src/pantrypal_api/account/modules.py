from injector import Binder, Module, singleton

from src.core.account.accessors.auth_token_accessor import IAuthTokenAccessor
from src.core.account.accessors.user_account_accessor import IUserAccountAccessor
from src.core.account.ports.auth_provider import IAuthProvider
from src.pantrypal_api.account.accessors.auth_token_accessor import AuthTokenAccessor
from src.pantrypal_api.account.accessors.user_account_accessor import (
    UserAccountAccessor,
)
from src.pantrypal_api.account.adapters.auth_provider import AuthProvider


class AccountModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IAuthProvider, to=AuthProvider, scope=singleton)
        binder.bind(IAuthTokenAccessor, to=AuthTokenAccessor, scope=singleton)
        binder.bind(IUserAccountAccessor, to=UserAccountAccessor, scope=singleton)
