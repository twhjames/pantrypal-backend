from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from src.core.chatbot.models import ChatHistoryDomain
from src.core.common.constants import SecretKey
from src.pantrypal_api.chatbot.accessors.chatbot_history_accessor import (
    ChatbotHistoryAccessor,
)


# Custom mock secret provider that returns a valid integer for CHATBOT_MAX_CHAT_HISTORY
@pytest.fixture
def mock_valid_secret_key_provider():
    provider = MagicMock()
    provider.get_secret.side_effect = (
        lambda key: "5" if key == SecretKey.CHATBOT_MAX_CHAT_HISTORY else "mock-secret"
    )
    return provider


# Test saving a single message and retrieving it from the DB
@pytest.mark.asyncio
async def test_save_and_retrieve_single_message(
    mock_relational_database_provider,
    mock_valid_secret_key_provider,
    mock_logging_provider,
):
    accessor = ChatbotHistoryAccessor(
        db_provider=mock_relational_database_provider,
        secret_provider=mock_valid_secret_key_provider,
        logging_provider=mock_logging_provider,
    )

    # Create a test message to save
    domain_msg = ChatHistoryDomain.create(
        user_id=1,
        role="user",
        content="What's in my fridge?",
        timestamp=datetime.now(timezone.utc),
        session_id=1,
    )

    # Save the message
    await accessor.save_message(domain_msg)

    # Retrieve recent messages for the user
    retrieved = await accessor.get_recent_messages(domain_msg.user_id, session_id=1)

    # Check that the saved message is among the results
    assert any(m.content == domain_msg.content for m in retrieved)


# Test saving multiple messages and retrieving them sorted by timestamp
@pytest.mark.asyncio
async def test_retrieve_multiple_messages_sorted_by_timestamp(
    mock_relational_database_provider,
    mock_valid_secret_key_provider,
    mock_logging_provider,
):
    accessor = ChatbotHistoryAccessor(
        db_provider=mock_relational_database_provider,
        secret_provider=mock_valid_secret_key_provider,
        logging_provider=mock_logging_provider,
    )

    # Create multiple messages with increasing timestamps
    messages = [
        ChatHistoryDomain.create(
            user_id=1,
            role="user",
            content="A",
            timestamp=datetime(2023, 1, 1, tzinfo=timezone.utc),
            session_id=1,
        ),
        ChatHistoryDomain.create(
            user_id=1,
            role="assistant",
            content="B",
            timestamp=datetime(2023, 1, 2, tzinfo=timezone.utc),
            session_id=1,
        ),
        ChatHistoryDomain.create(
            user_id=1,
            role="user",
            content="C",
            timestamp=datetime(2023, 1, 3, tzinfo=timezone.utc),
            session_id=1,
        ),
    ]

    # Save all messages
    for msg in messages:
        await accessor.save_message(msg)

    # Retrieve and assert the messages are returned in correct order
    retrieved = await accessor.get_recent_messages(1, session_id=1)
    assert len(retrieved) == 3
    assert [m.content for m in retrieved] == ["C", "B", "A"]
