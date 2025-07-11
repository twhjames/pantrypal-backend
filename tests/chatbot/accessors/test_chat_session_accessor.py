import pytest

from src.core.chatbot.models import ChatSessionDomain
from src.pantrypal_api.chatbot.accessors.chat_session_accessor import (
    ChatSessionAccessor,
)


@pytest.mark.asyncio
async def test_create_and_list_sessions(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = ChatSessionAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    domain = ChatSessionDomain.create(
        user_id=1,
        title="Soup",
        summary="Tasty",
        prep_time=15,
        instructions=["step"],
        ingredients=["water"],
        available_ingredients=1,
        total_ingredients=1,
    )

    created = await accessor.create_session(domain)
    assert created.title == "Soup"

    sessions = await accessor.list_sessions(1)
    assert any(s.title == "Soup" for s in sessions)


@pytest.mark.asyncio
async def test_update_session_recipe(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = ChatSessionAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    domain = ChatSessionDomain.create(
        user_id=1,
        title="Soup",
        summary="Tasty",
        prep_time=15,
        instructions=["step"],
        ingredients=["water"],
        available_ingredients=1,
        total_ingredients=1,
    )

    created = await accessor.create_session(domain)

    updated_spec = domain.model_copy(
        update={"title": "Stew", "instructions": ["cook"], "ingredients": ["beef"]}
    )
    updated = await accessor.update_session_recipe(created.id, updated_spec)

    assert updated.title == "Stew"
    assert updated.instructions == ["cook"]
