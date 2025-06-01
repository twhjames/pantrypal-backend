from abc import ABC, abstractmethod
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


class IDatabaseProvider(ABC):
    @abstractmethod
    def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield an async DB session."""
        raise NotImplementedError
