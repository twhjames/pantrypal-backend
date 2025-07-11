import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestChatbotEndpoints:
    async def test_recommend_endpoint(self, async_client: AsyncClient):
        payload = {
            "user_id": 1,
            "role": "user",
            "content": "I have salmon and broccoli",
            "timestamp": "2025-06-01T15:01:03.110Z",
            "session_id": 1,
        }

        response = await async_client.post("/chatbot/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data

    async def test_chat_endpoint(self, async_client: AsyncClient):
        payload = {
            "user_id": 1,
            "role": "user",
            "content": "What can I cook today?",
            "timestamp": "2025-06-01T15:01:03.110Z",
            "session_id": 1,
        }

        response = await async_client.post("/chatbot/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "reply" in data
