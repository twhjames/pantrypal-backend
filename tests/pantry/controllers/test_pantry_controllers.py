import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPantryEndpoints:
    async def test_add_items(self, async_client: AsyncClient):
        # create user and login to obtain token
        await async_client.post(
            "/account/register",
            json={
                "username": "pantry",
                "email": "pantry@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "pantry@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        payload = [
            {
                "item_name": "Milk",
                "quantity": 2,
                "unit": "liters",
                "category": "Dairy",
                "purchase_date": "2025-06-01T10:00:00Z",
                "expiry_date": "2025-06-05T10:00:00Z",
            }
        ]
        response = await async_client.post(
            "/pantry/add",
            json=payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["item_name"] == "Milk"
        assert data[0]["unit"] == "liters"
        assert data[0]["category"] == "Dairy"

    async def test_list_items(self, async_client: AsyncClient):
        await async_client.post(
            "/account/register",
            json={
                "username": "pantry",
                "email": "pantry@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "pantry@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        response = await async_client.get(
            "/pantry/list",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_update_item(self, async_client: AsyncClient):
        # add the item
        await async_client.post(
            "/account/register",
            json={
                "username": "pantry",
                "email": "pantry@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "pantry@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        add_payload = {
            "item_name": "Milk (Low Fat)",
            "quantity": 1,
            "unit": "liters",
            "category": "Dairy",
            "purchase_date": "2025-06-01T10:00:00Z",
            "expiry_date": "2025-06-07T10:00:00Z",
        }

        response = await async_client.post(
            "/pantry/add",
            json=[add_payload],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        item_id = response.json()[0]["id"]

        # update that item
        update_payload = {
            "item_id": item_id,
            "item_name": "Milk (Skimmed)",
            "quantity": 1,
            "unit": "liters",
            "category": "Dairy",
            "purchase_date": "2025-06-01T10:00:00Z",
            "expiry_date": "2025-06-07T10:00:00Z",
        }

        update_response = await async_client.patch(
            "/pantry/update",
            json=update_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert update_response.status_code == 200
        assert update_response.json()["item_name"] == "Milk (Skimmed)"

    async def test_delete_item(self, async_client: AsyncClient):
        # add the item
        await async_client.post(
            "/account/register",
            json={
                "username": "pantry",
                "email": "pantry@example.com",
                "password": "pass123",
            },
        )
        login_resp = await async_client.post(
            "/account/login",
            json={"email": "pantry@example.com", "password": "pass123"},
        )
        token = login_resp.json()["token"]

        add_payload = {
            "item_name": "Milk (Low Fat)",
            "quantity": 1,
            "unit": "liters",
            "category": "Dairy",
            "purchase_date": "2025-06-01T10:00:00Z",
            "expiry_date": "2025-06-07T10:00:00Z",
        }

        response = await async_client.post(
            "/pantry/add",
            json=[add_payload],
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

        item_id = response.json()[0]["id"]

        # delete the item
        delete_payload = {"item_ids": [item_id]}

        delete_response = await async_client.post(
            url="/pantry/delete",
            json=delete_payload,
            headers={"Authorization": f"Bearer {token}"},
        )
        assert delete_response.status_code == 204

        list_response = await async_client.get(
            "/pantry/list",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_response.status_code == 200
        items = list_response.json()
        assert all(item["id"] != item_id for item in items)
