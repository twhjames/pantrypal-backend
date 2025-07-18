from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient

from src.core.chatbot.models import ChatHistoryDomain, ChatSessionDomain
from src.core.common.constants import SecretKey
from src.core.common.utils import DateTimeUtils
from src.pantrypal_api.chatbot.accessors.chat_session_accessor import (
    ChatSessionAccessor,
)
from src.pantrypal_api.chatbot.accessors.chatbot_history_accessor import (
    ChatbotHistoryAccessor,
)


@pytest.fixture
def mock_valid_secret_key_provider():
    provider = MagicMock()
    provider.get_secret.side_effect = lambda key: (
        "5" if key == SecretKey.CHATBOT_MAX_CHAT_HISTORY else "secret"
    )
    return provider


@pytest.mark.asyncio
class TestChatSessionEndpoints:
    async def test_list_sessions(self, async_client: AsyncClient):
        await async_client.post(
            "/account/register",
            json={
                "username": "chat",
                "email": "chat@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "chat@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.get(
            "/chatbot/sessions",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_session_history(self, async_client: AsyncClient):
        await async_client.post(
            "/account/register",
            json={
                "username": "hist",
                "email": "hist@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "hist@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.get(
            "/chatbot/sessions/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_delete_session(
        self,
        async_client: AsyncClient,
        mock_relational_database_provider,
        mock_valid_secret_key_provider,
        mock_logging_provider,
    ):
        session_accessor = ChatSessionAccessor(
            db_provider=mock_relational_database_provider,
            logging_provider=mock_logging_provider,
        )
        history_accessor = ChatbotHistoryAccessor(
            db_provider=mock_relational_database_provider,
            secret_provider=mock_valid_secret_key_provider,
            logging_provider=mock_logging_provider,
        )

        session_domain = ChatSessionDomain.create(user_id=1, title="Test")
        created = await session_accessor.create_session(session_domain)

        msg = ChatHistoryDomain.create(
            user_id=1,
            role="user",
            content="hi",
            timestamp=DateTimeUtils.get_utc_now(),
            session_id=created.id,
        )
        await history_accessor.save_message(msg)

        await async_client.post(
            "/account/register",
            json={
                "username": "del",
                "email": "del@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "del@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.delete(
            f"/chatbot/sessions/{created.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204
