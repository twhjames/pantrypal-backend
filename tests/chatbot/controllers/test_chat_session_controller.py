import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestChatSessionEndpoints:
    async def test_list_sessions(self, async_client: AsyncClient):
        response = await async_client.get("/chatbot/sessions?user_id=1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_session_history(self, async_client: AsyncClient):
        response = await async_client.get("/chatbot/sessions/1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
