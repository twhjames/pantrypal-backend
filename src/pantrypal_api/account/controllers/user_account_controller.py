from injector import inject

from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.account.schemas.user_account_schemas import (
    AuthTokenOut,
    LoginUserIn,
    RegisterUserIn,
    UpdateUserIn,
    UserOut,
)


class UserAccountController:
    @inject
    def __init__(self, auth_service: AuthService, user_service: UserAccountService):
        self.auth_service = auth_service
        self.user_service = user_service

    async def register_user(self, data: RegisterUserIn) -> UserOut:
        spec = data.to_spec()
        user_account_domain = await self.user_service.register_user(spec)
        return user_account_domain.to_schema()

    async def login(self, data: LoginUserIn) -> AuthTokenOut:
        spec = data.to_spec()
        auth_token_domain = await self.auth_service.login(spec)
        return auth_token_domain.to_schema()

    async def update_user(self, user_id: int, data: UpdateUserIn) -> UserOut:
        spec = data.to_spec()
        updated_user_domain = await self.user_service.update_user(user_id, spec)
        return updated_user_domain.to_schema()

    async def delete_user(self, user_id: int) -> None:
        await self.user_service.delete_user(user_id)

    async def logout(self, token: str) -> None:
        await self.auth_service.logout(token)
