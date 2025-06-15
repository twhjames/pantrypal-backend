from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.app.main import app
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.base.models import PantryPalBaseModel

"""
conftest.py — Shared test fixtures for the PantryPal FastAPI application.

This setup includes:
- Mock providers for interface-based dependencies (e.g., Auth, Chatbot)
- AsyncMock-based accessors for testing async services
- MagicMock-based accessors for testing sync services
- SQLite in-memory test DB for integration tests
- ASGI-compatible HTTP client for controller tests
"""

# ===============================
# MOCK PROVIDERS (Ports / Services)
# ===============================


# Mock ILogginerProvider using MagicMock
@pytest.fixture
def mock_logging_provider():
    return MagicMock(spec=ILoggingProvider)


# Mock IDatabaseProvider using MagicMock with async get_db() support and injected logging provider
@pytest_asyncio.fixture
async def mock_relational_database_provider(db_session, mock_logging_provider):
    provider = MagicMock(spec=IDatabaseProvider)

    @asynccontextmanager
    async def mock_get_db():
        yield db_session

    provider.get_db.side_effect = mock_get_db
    provider.logging_provider = mock_logging_provider
    return provider


# Mock IAuthProvider using MagicMock since all methods are synchronous
@pytest.fixture
def mock_auth_provider():
    provider = MagicMock()
    provider.get_hashed_password.return_value = "securehash"
    provider.verify_password.return_value = True
    provider.generate_jwt.return_value = "mock.jwt.token"
    provider.decode_jwt.return_value = {"sub": "1"}
    return provider


# Mock IChatbotProvider for tests needing chatbot replies
@pytest.fixture
def mock_chatbot_provider():
    provider = MagicMock(spec=IChatbotProvider)
    provider.handle_single_turn = AsyncMock(return_value="Mocked reply")
    provider.handle_multi_turn = AsyncMock(return_value="Mocked context reply")
    return provider


# Mock ISecretKeyProvider for JWT and config access
@pytest.fixture
def mock_secret_key_provider(mock_logging_provider):
    provider = MagicMock(spec=ISecretProvider)
    return provider


# ===============================
# MOCK ACCESSORS (for Domain Layer)
# ===============================


# Helper for creating async-mocked accessors
def make_async_accessor(methods: list[str]):
    accessor = MagicMock()
    for method in methods:
        setattr(accessor, method, AsyncMock())
    return accessor


# Helper for creating sync-mocked accessors
def make_sync_accessor(methods: list[str]):
    accessor = MagicMock()
    for method in methods:
        setattr(accessor, method, MagicMock())
    return accessor


# Async-mocked accessors (used in async service testing)
@pytest.fixture
def mock_user_account_accessor():
    return make_async_accessor(
        ["get_by_id", "get_by_email", "create_user", "update_user", "delete_by_id"]
    )


@pytest.fixture
def mock_auth_token_accessor():
    return make_async_accessor(
        ["get_by_token", "upsert", "delete_by_token", "delete_by_user_id"]
    )


@pytest.fixture
def mock_chat_history_accessor():
    return make_async_accessor(["get_recent_messages", "save_message"])


@pytest.fixture
def mock_pantry_item_accessor():
    return make_async_accessor(
        [
            "get_items_by_user",
            "add_items",
            "get_item_by_id",
            "update_item",
            "delete_items",
            "get_items_by_ids",
        ]
    )


# Sync-mocked accessors (used in sync service testing)
@pytest.fixture
def mock_configuration_accessor():
    return make_async_accessor(["get_by_key"])


# ===============================
# TEST DATABASE SETUP (In-Memory SQLite)
# ===============================

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL, future=True)
TestingSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(PantryPalBaseModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(PantryPalBaseModel.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def clean_all_tables(db_session):
    for table in reversed(PantryPalBaseModel.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()


# ===============================
# HTTP CLIENT FOR CONTROLLER TESTS
# ===============================


@pytest_asyncio.fixture
async def async_client():
    """
    Provides an AsyncClient that communicates with the FastAPI app via ASGITransport.
    Used for testing API endpoint behavior in controller tests.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
