from sqlalchemy import Column, DateTime, Integer, String

from src.core.account.models import AuthTokenDomain, UserAccountDomain
from src.pantrypal_api.base.models import PantryPalBaseModel


class UserAccount(PantryPalBaseModel):
    __tablename__ = "user_accounts"

    username = Column(String)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    def to_domain(self) -> UserAccountDomain:
        return UserAccountDomain(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            email=self.email,
            password_hash=self.password_hash,
        )


class AuthToken(PantryPalBaseModel):
    __tablename__ = "auth_tokens"

    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True)
    token_issued_at = Column(DateTime)
    expires_at = Column(DateTime)

    def to_domain(self) -> AuthTokenDomain:
        return AuthTokenDomain(
            id=self.id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            token=self.token,
            user_id=self.user_id,
            token_issued_at=self.token_issued_at,
            expires_at=self.expires_at,
        )
