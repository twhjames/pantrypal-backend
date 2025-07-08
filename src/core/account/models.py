from datetime import datetime

from src.core.base.models import PantryPalBaseModelDomain, PantryPalMutableModelDomain
from src.pantrypal_api.account.schemas.user_account_schemas import AuthTokenOut, UserOut


class UserAccountDomain(PantryPalMutableModelDomain):
    username: str
    email: str
    password_hash: str

    def to_schema(self) -> UserOut:
        return UserOut(
            id=self.id,
            username=self.username,
            email=self.email,
            created_at=self.created_at,
        )

    @classmethod
    def create(
        cls, username: str, email: str, password_hash: str
    ) -> "UserAccountDomain":
        return cls(
            id=0,  # placeholder before DB insert
            username=username,
            email=email,
            password_hash=password_hash,
        )


class AuthTokenDomain(PantryPalBaseModelDomain):
    token: str
    user_id: int
    token_issued_at: datetime
    expires_at: datetime

    def to_schema(self) -> AuthTokenOut:
        return AuthTokenOut(
            user_id=self.user_id,
            token=self.token,
            expires_at=self.expires_at,
        )

    @classmethod
    def create(
        cls, token: str, user_id: int, token_issued_at: datetime, expires_at: datetime
    ) -> "AuthTokenDomain":
        return cls(
            id=0,  # placeholder before DB insert
            token=token,
            user_id=user_id,
            token_issued_at=token_issued_at,
            expires_at=expires_at,
        )
