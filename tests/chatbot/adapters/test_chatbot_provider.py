from datetime import datetime, timezone

import pytest

from src.core.chatbot.specs import ChatMessageSpec
from src.pantrypal_api.chatbot.adapters.chatbot_provider import GroqChatbotProvider


# Real GroqChatbotProvider with mocked dependencies for unit testing adapter logic
@pytest.fixture
def groq_chatbot_provider(mock_secret_key_provider, mock_logging_provider):
    return GroqChatbotProvider(
        secret_provider=mock_secret_key_provider,
        logging_provider=mock_logging_provider,
    )


@pytest.mark.asyncio
async def test_handle_single_turn_calls_sync(monkeypatch, groq_chatbot_provider):
    mock_response = "Mocked reply"
    monkeypatch.setattr(
        groq_chatbot_provider,
        "_GroqChatbotProvider__sync_call_groq",
        lambda formatted_messages: mock_response,
    )

    message = ChatMessageSpec(
        user_id=1,
        role="user",
        content="What can I cook?",
        timestamp=datetime.now(timezone.utc),
    )

    result = await groq_chatbot_provider.handle_single_turn(message)
    assert result == mock_response


@pytest.mark.asyncio
async def test_handle_multi_turn_calls_sync(monkeypatch, groq_chatbot_provider):
    mock_response = "Mocked context reply"
    monkeypatch.setattr(
        groq_chatbot_provider,
        "_GroqChatbotProvider__sync_call_groq",
        lambda formatted_messages: mock_response,
    )

    now = datetime.now(timezone.utc)
    messages = [
        ChatMessageSpec(
            user_id=1, role="user", content="What's in the fridge?", timestamp=now
        ),
        ChatMessageSpec(
            user_id=1, role="assistant", content="Eggs and rice", timestamp=now
        ),
    ]

    result = await groq_chatbot_provider.handle_multi_turn(messages)
    assert result == mock_response
