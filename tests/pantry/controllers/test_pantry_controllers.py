import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestPantryEndpoints:
    async def test_add_items(self, async_client: AsyncClient):
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
        response = await async_client.post("/pantry/add?user_id=1", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["item_name"] == "Milk"
        assert data[0]["unit"] == "liters"
        assert data[0]["category"] == "Dairy"

    async def test_list_items(self, async_client: AsyncClient):
        response = await async_client.get("/pantry/list?user_id=1")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    async def test_update_item(self, async_client: AsyncClient):
        # add the item
        add_payload = {
            "item_name": "Milk (Low Fat)",
            "quantity": 1,
            "unit": "liters",
            "category": "Dairy",
            "purchase_date": "2025-06-01T10:00:00Z",
            "expiry_date": "2025-06-07T10:00:00Z",
        }

        response = await async_client.post("/pantry/add?user_id=1", json=[add_payload])
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
            "/pantry/update?user_id=1", json=update_payload
        )
        assert update_response.status_code == 200
        assert update_response.json()["item_name"] == "Milk (Skimmed)"

    async def test_delete_item(self, async_client: AsyncClient):
        # add the item
        add_payload = {
            "item_name": "Milk (Low Fat)",
            "quantity": 1,
            "unit": "liters",
            "category": "Dairy",
            "purchase_date": "2025-06-01T10:00:00Z",
            "expiry_date": "2025-06-07T10:00:00Z",
        }

        response = await async_client.post("/pantry/add?user_id=1", json=[add_payload])
        assert response.status_code == 200

        item_id = response.json()[0]["id"]

        # delete the item
        delete_payload = {"item_ids": [item_id]}

        delete_response = await async_client.post(
            url="/pantry/delete?user_id=1", json=delete_payload
        )
        assert delete_response.status_code == 204

        list_response = await async_client.get("/pantry/list?user_id=1")
        assert list_response.status_code == 200
        items = list_response.json()
        assert all(item["id"] != item_id for item in items)
