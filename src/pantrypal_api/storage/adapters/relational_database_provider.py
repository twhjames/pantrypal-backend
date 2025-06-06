from contextlib import asynccontextmanager
from typing import AsyncGenerator

from injector import inject
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider


class RelationalDatabaseProvider(IDatabaseProvider):
    """Provides async DB sessions using SQLAlchemy."""

    @inject
    def __init__(
        self,
        secret_provider: ISecretProvider,
        logging_provider: ILoggingProvider,
    ):
        self.logging_provider = logging_provider
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
            except Exception as e:
                await session.rollback()
                self.logging_provider.error(
                    "Database session rolled back due to exception",
                    extra_data={"error": str(e)},
                    tag="Database",
                )
                raise
            finally:
                await session.close()
                self.logging_provider.debug("Database session closed", tag="Database")
