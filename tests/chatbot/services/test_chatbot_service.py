from datetime import datetime, timezone

import pytest

from src.core.chatbot.models import ChatHistoryDomain, ChatSessionDomain
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

    created_session = ChatSessionDomain.create(user_id=1, title="Soup")
    created_session.id = 1
    mock_chat_session_service.create_session.return_value = created_session

    msg = ChatMessageSpec(
        id=1,
        role="user",
        content="I have tomatoes and pasta",
        user_id=1,
        timestamp=datetime.now(timezone.utc),
        session_id=1,
    )
    reply, session_id = await service.get_first_recommendation(msg)

    assert reply == '{"title": "Soup", "ingredients": [], "instructions": []}'
    assert session_id == 1
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
    reply, session_id = await service.get_first_recommendation(msg)

    mock_chat_session_service.create_session.assert_awaited()
    assert reply == '{"title": "Soup", "ingredients": [], "instructions": []}'
    assert session_id == mock_chat_session_service.create_session.return_value.id


@pytest.mark.asyncio
async def test_first_recommendation_saves_user_message_with_session(
    mock_chatbot_provider,
    mock_chatbot_history_accessor,
    mock_pantry_service,
    mock_chat_session_service,
    mock_logging_provider,
):
    mock_chatbot_provider.handle_multi_turn.return_value = (
        '{"title": "Soup", "ingredients": [], "instructions": []}'
    )
    created_session = ChatSessionDomain.create(user_id=1, title="Soup")
    created_session.id = 123
    mock_chat_session_service.create_session.return_value = created_session

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
    )
    reply, session_id = await service.get_first_recommendation(msg)

    saved_user_message = mock_chatbot_history_accessor.save_message.await_args_list[
        0
    ].args[0]
    assert saved_user_message.session_id == 123
    assert session_id == 123


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


@pytest.mark.asyncio
async def test_get_recipe_title_suggestions(
    mock_chatbot_provider,
    mock_chatbot_history_accessor,
    mock_pantry_service,
    mock_chat_session_service,
    mock_logging_provider,
):
    mock_chatbot_provider.handle_single_turn.return_value = '["A", "B", "C", "D"]'

    service = ChatbotService(
        chatbot_provider=mock_chatbot_provider,
        chatbot_history_accessor=mock_chatbot_history_accessor,
        pantry_service=mock_pantry_service,
        chat_session_service=mock_chat_session_service,
        logging_provider=mock_logging_provider,
    )

    result = await service.get_recipe_title_suggestions(1)

    assert result == ["A", "B", "C", "D"]
    mock_chatbot_provider.handle_single_turn.assert_awaited_once()
