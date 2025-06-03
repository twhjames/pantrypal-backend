from abc import ABC, abstractmethod

from src.core.account.models import AuthTokenDomain


class IAuthTokenAccessor(ABC):
    @abstractmethod
    async def upsert(self, auth_token: AuthTokenDomain) -> AuthTokenDomain:
        """
        Create or update the auth token entry for a user.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_token(self, token: str) -> AuthTokenDomain | None:
        """
        Retrieve the auth token domain object by token string.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_token(self, token: str) -> None:
        """
        Deletes a token entry using the token (hashed token string).
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_by_user_id(self, user_id: int) -> None:
        """
        Deletes all tokens for a given user.
        """
        raise NotImplementedError
