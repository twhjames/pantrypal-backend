from injector import inject

from src.core.account.accessors.auth_token_accessor import IAuthTokenAccessor
from src.core.account.accessors.user_account_accessor import IUserAccountAccessor
from src.core.account.models import UserAccountDomain
from src.core.account.ports.auth_provider import IAuthProvider
from src.core.account.specs import RegisterUserSpec, UpdateUserSpec


class UserAccountService:
    """Handles operations related to user account lifecycle."""

    @inject
    def __init__(
        self,
        user_account_accessor: IUserAccountAccessor,
        auth_provider: IAuthProvider,
        auth_token_accessor: IAuthTokenAccessor,
    ):
        self.user_account_accessor = user_account_accessor
        self.auth_provider = auth_provider
        self.auth_token_accessor = auth_token_accessor

    async def register_user(self, spec: RegisterUserSpec) -> UserAccountDomain:
        if await self.user_account_accessor.get_by_email(spec.email):
            raise ValueError("A user with this email already exists")

        hashed_password = self.auth_provider.get_hashed_password(spec.password)

        user = UserAccountDomain.create(
            username=spec.username, email=spec.email, password_hash=hashed_password
        )

        return await self.user_account_accessor.create_user(user)

    async def update_user(
        self, user_id: int, spec: UpdateUserSpec
    ) -> UserAccountDomain:
        user = await self.user_account_accessor.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if spec.username:
            user.username = spec.username
        if spec.email:
            user.email = spec.email
        if spec.password:
            user.password_hash = self.auth_provider.get_hashed_password(spec.password)

        return await self.user_account_accessor.update_user(user)

    async def delete_user(self, user_id: int) -> None:
        user = await self.user_account_accessor.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        await self.auth_token_accessor.delete_by_user_id(user_id)
        await self.user_account_accessor.delete_by_id(user_id)
