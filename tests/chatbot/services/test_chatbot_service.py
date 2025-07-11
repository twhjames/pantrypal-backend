from datetime import datetime, timezone

import pytest

from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.services.chatbot_service import ChatbotService
from src.core.chatbot.specs import ChatMessageSpec


@pytest.mark.asyncio
async def test_get_first_recommendation(
    mock_chatbot_provider,
    mock_chatbot_history_accessor,
    mock_pantry_service,
    mock_chat_session_service,
    mock_logging_provider,
):
    mock_chatbot_provider.handle_multi_turn.return_value = (
        '{"title": "Soup", "ingredients": [], "instructions": []}'
    )

    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chatbot_history_accessor=mock_chatbot_history_accessor,
        pantry_service=mock_pantry_service,
        chat_session_service=mock_chat_session_service,
        logging_provider=mock_logging_provider,
    )

    msg = ChatMessageSpec(
        id=1,
        role="user",
        content="I have tomatoes and pasta",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
        session_id=1,
    )
    result = await service.get_first_recommendation(msg)

    assert result == '{"title": "Soup", "ingredients": [], "instructions": []}'
    mock_chat_session_service.update_session_recipe.assert_awaited()
    assert mock_chatbot_history_accessor.save_message.await_count == 2


@pytest.mark.asyncio
async def test_get_first_recommendation_creates_session(
    mock_chatbot_provider,
    mock_chatbot_history_accessor,
    mock_pantry_service,
    mock_chat_session_service,
    mock_logging_provider,
):
    mock_chatbot_provider.handle_multi_turn.return_value = (
        '{"title": "Soup", "ingredients": [], "instructions": []}'
    )

    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chatbot_history_accessor=mock_chatbot_history_accessor,
        pantry_service=mock_pantry_service,
        chat_session_service=mock_chat_session_service,
        logging_provider=mock_logging_provider,
    )

    msg = ChatMessageSpec(
        role="user",
        content="I have tomatoes and pasta",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
        session_id=None,
    )
    await service.get_first_recommendation(msg)

    mock_chat_session_service.create_session.assert_awaited()


@pytest.mark.asyncio
async def test_chat_with_context(
    mock_chatbot_provider,
    mock_chatbot_history_accessor,
    mock_pantry_service,
    mock_chat_session_service,
    mock_logging_provider,
):
    mock_chatbot_history_accessor.get_recent_messages.return_value = [
        ChatHistoryDomain.create(
            user_id=1,
            role="user",
            content="I have eggs",
            timestamp=datetime.now(timezone.utc),
            session_id=1,
        ),
        ChatHistoryDomain.create(
            user_id=1,
            role="assistant",
            content="Make an omelette",
            timestamp=datetime.now(timezone.utc),
            session_id=1,
        ),
    ]

    mock_chatbot_provider.handle_multi_turn.return_value = (
        '{"title": "Rice", "ingredients": [], "instructions": []}'
    )

    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chatbot_history_accessor=mock_chatbot_history_accessor,
        pantry_service=mock_pantry_service,
        chat_session_service=mock_chat_session_service,
        logging_provider=mock_logging_provider,
    )

    new_msg = ChatMessageSpec(
        role="user",
        content="Now I have rice",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
        session_id=1,
    )
    result = await service.chat_with_context(new_msg)

    assert result == '{"title": "Rice", "ingredients": [], "instructions": []}'
    mock_chatbot_provider.handle_multi_turn.assert_awaited()
    mock_chatbot_history_accessor.get_recent_messages.assert_awaited_once()
    mock_chatbot_history_accessor.save_message.assert_awaited()
    mock_chat_session_service.update_session_recipe.assert_awaited()
