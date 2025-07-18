import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestChatbotEndpoints:
    async def test_recommend_endpoint(self, async_client: AsyncClient):
        await async_client.post(
            "/account/register",
            json={
                "username": "rec",
                "email": "rec@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "rec@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        payload = {
            "role": "user",
            "content": "I have salmon and broccoli",
            "timestamp": "2025-06-01T15:01:03.110Z",
            "session_id": 1,
        }

        response = await async_client.post(
            "/chatbot/recommend",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
        assert "session_id" in data

    async def test_chat_endpoint(self, async_client: AsyncClient):
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

        payload = {
            "role": "user",
            "content": "What can I cook today?",
            "timestamp": "2025-06-01T15:01:03.110Z",
            "session_id": 1,
        }

        response = await async_client.post(
            "/chatbot/chat",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data

    async def test_title_suggestions_endpoint(
        self, async_client: AsyncClient, monkeypatch
    ):
        async def fake_single_turn(self, message):
            return '["One", "Two", "Three", "Four"]'

        monkeypatch.setattr(
            "src.pantrypal_api.chatbot.adapters.chatbot_provider.GroqChatbotProvider.handle_single_turn",
            fake_single_turn,
        )

        await async_client.post(
            "/account/register",
            json={
                "username": "titles",
                "email": "titles@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "titles@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.get(
            "/chatbot/title-suggestions",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data.get("suggestions"), list)
        assert len(data["suggestions"]) == 4
