from datetime import datetime, timezone

import pytest

from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.services.chatbot_service import ChatbotService


@pytest.mark.asyncio
async def test_get_first_recommendation(
    mock_chatbot_provider, mock_chat_history_accessor
):
    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chat_history_accessor=mock_chat_history_accessor,
    )

    msg = ChatHistoryDomain(
        id=1,
        role="user",
        content="I have tomatoes and pasta",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
    )
    result = await service.get_first_recommendation(msg)

    assert result == "Mocked reply: Try making fried rice."


@pytest.mark.asyncio
async def test_chat_with_context(mock_chatbot_provider, mock_chat_history_accessor):
    mock_chat_history_accessor.get_recent_messages.return_value = [
        ChatHistoryDomain(
            id=1,
            role="user",
            content="I have eggs",
            user_id=1,
            timestamp=datetime.now(timezone.utc),
        ),
        ChatHistoryDomain(
            id=2,
            role="assistant",
            content="Make an omelette",
            user_id=1,
            timestamp=datetime.now(timezone.utc),
        ),
    ]

    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chat_history_accessor=mock_chat_history_accessor,
    )

    new_msg = ChatHistoryDomain(
        id=3,
        role="user",
        content="Now I have rice",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
    )
    result = await service.chat_with_context(new_msg)

    assert result == "Mocked chat: Here's what I suggest..."
    mock_chatbot_provider.handle_multi_turn.assert_awaited()
    mock_chat_history_accessor.get_recent_messages.assert_awaited_once()
    mock_chat_history_accessor.save_message.assert_awaited()
