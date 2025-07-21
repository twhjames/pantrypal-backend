from uuid import uuid4  # for generating unique emails

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserAccountEndpoints:
    """
    Integration tests for user account API endpoints.
    These simulate real HTTP interactions using FastAPI + httpx.AsyncClient.
    """

    async def test_register_user(self, async_client: AsyncClient):
        email = f"{uuid4()}@example.com"
        payload = {"username": "testuser", "email": email, "password": "password123"}

        response = await async_client.post("/account/register", json=payload)
        assert response.status_code == 200
        data = response.json()

        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert "id" in data
        assert data["is_admin"] is False

    async def test_login_user(self, async_client: AsyncClient):
        email = f"{uuid4()}@example.com"
        await async_client.post(
            "/account/register",
            json={"username": "loginuser", "email": email, "password": "password123"},
        )

        payload = {"email": email, "password": "password123"}

        response = await async_client.post("/account/login", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "token" in data

    async def test_update_user(self, async_client: AsyncClient):
        email = f"{uuid4()}@example.com"
        register_payload = {
            "username": "updateuser",
            "email": email,
            "password": "password123",
        }
        register_response = await async_client.post(
            "/account/register", json=register_payload
        )
        assert register_response.status_code == 200
        # login to obtain auth token
        login_payload = {"email": email, "password": "password123"}
        login_response = await async_client.post("/account/login", json=login_payload)
        token = login_response.json()["token"]

        updated_email = f"{uuid4()}@example.com"
        update_payload = {
            "username": "updateduser",
            "email": updated_email,
            "password": "newpassword123",
        }

        response = await async_client.put(
            "/account/update",
            json=update_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == update_payload["username"]
        assert data["email"] == update_payload["email"]

    async def test_logout_user(self, async_client: AsyncClient):
        email = f"{uuid4()}@example.com"
        await async_client.post(
            "/account/register",
            json={"username": "logoutuser", "email": email, "password": "password123"},
        )

        login_payload = {"email": email, "password": "password123"}
        login_response = await async_client.post("/account/login", json=login_payload)
        assert login_response.status_code == 200
        token = login_response.json()["token"]

        response = await async_client.post(
            "/account/logout",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["detail"] == "Logged out successfully"

    async def test_delete_user(self, async_client: AsyncClient):
        email = f"{uuid4()}@example.com"
        register_payload = {
            "username": "deleteuser",
            "email": email,
            "password": "password123",
        }
        register_response = await async_client.post(
            "/account/register", json=register_payload
        )
        assert register_response.status_code == 200
        login_payload = {"email": email, "password": "password123"}
        login_response = await async_client.post("/account/login", json=login_payload)
        token = login_response.json()["token"]

        response = await async_client.delete(
            "/account/delete",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["detail"] == "User deleted successfully"
