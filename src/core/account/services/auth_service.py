from fastapi import HTTPException, status
from injector import inject

from src.core.account.accessors.auth_token_accessor import IAuthTokenAccessor
from src.core.account.accessors.user_account_accessor import IUserAccountAccessor
from src.core.account.models import AuthTokenDomain
from src.core.account.ports.auth_provider import IAuthProvider
from src.core.account.specs import LoginSpec
from src.core.common.utils import DateTimeUtils


class AuthService:
    """Handles user login, logout, and token lifecycle management."""

    @inject
    def __init__(
        self,
        auth_provider: IAuthProvider,
        user_accessor: IUserAccountAccessor,
        token_accessor: IAuthTokenAccessor,
    ):
        self.auth_provider = auth_provider
        self.user_accessor = user_accessor
        self.token_accessor = token_accessor

    async def login(self, spec: LoginSpec) -> AuthTokenDomain:
        user = await self.user_accessor.get_by_email(spec.email)
        if not user or not self.auth_provider.verify_password(
            spec.password, user.password_hash
        ):
            raise ValueError("Invalid email or password")

        return await self.create_auth_token(user.id)

    async def create_auth_token(self, user_id: int) -> AuthTokenDomain:
        token = self.auth_provider.generate_token(user_id)
        now = DateTimeUtils.get_utc_now()
        expires = DateTimeUtils.add_minutes(now, 60 * 24 * 7)

        auth_token = AuthTokenDomain.create(
            token=token,
            user_id=user_id,
            token_issued_at=now,
            expires_at=expires,
        )

        return await self.token_accessor.upsert(auth_token)

    async def logout(self, token: str) -> None:
        auth_token = await self.token_accessor.get_by_token(token)
        if not auth_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        await self.token_accessor.delete_by_token(token)

    async def invalidate_user_tokens(self, user_id: int) -> None:
        await self.token_accessor.delete_by_user_id(user_id)
