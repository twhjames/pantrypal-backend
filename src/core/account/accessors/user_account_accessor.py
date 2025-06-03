from abc import ABC, abstractmethod
from typing import Optional

from src.core.account.models import UserAccountDomain


class IUserAccountAccessor(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[UserAccountDomain]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[UserAccountDomain]:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: UserAccountDomain) -> UserAccountDomain:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: UserAccountDomain) -> UserAccountDomain:
        raise NotImplementedError
