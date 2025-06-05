from contextlib import asynccontextmanager
from typing import AsyncGenerator

from injector import inject
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider


class RelationalDatabaseProvider(IDatabaseProvider):
    """Provides async DB sessions using SQLAlchemy."""

    @inject
    def __init__(self, secret_provider: ISecretProvider):
        db_url = secret_provider.get_secret(SecretKey.DATABASE_URL)
        self.engine = create_async_engine(db_url, echo=False)
        self.async_session_factory = sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    @asynccontextmanager
    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        """Yield an async DB session."""
        async with self.async_session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
