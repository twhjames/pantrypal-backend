from typing import List

from injector import inject

from src.core.pantry.services.pantry_service import PantryService
from src.pantrypal_api.pantry.schemas.pantry_schemas import (
    AddPantryItemRequest,
    DeletePantryItemsRequest,
    PantryItemResponse,
    PantryStatsResponse,
    UpdatePantryItemRequest,
)


class PantryController:
    @inject
    def __init__(self, pantry_service: PantryService):
        self.pantry_service = pantry_service

    async def get_items(self, user_id: int) -> List[PantryItemResponse]:
        result = await self.pantry_service.get_items(user_id)
        return [item.to_schema() for item in result]

    async def add_items(
        self, user_id: int, data: List[AddPantryItemRequest]
    ) -> List[PantryItemResponse]:
        specs = [req.to_spec() for req in data]
        result = await self.pantry_service.add_items(user_id, specs)
        return [item.to_schema() for item in result]

    async def update_item(
        self, user_id: int, data: UpdatePantryItemRequest
    ) -> PantryItemResponse:
        spec = data.to_spec()
        updated = await self.pantry_service.update_item(user_id, spec)
        return updated.to_schema()

    async def delete_items(self, user_id: int, data: DeletePantryItemsRequest) -> None:
        spec = data.to_spec()
        await self.pantry_service.delete_items(user_id, spec)

    async def get_stats(self, user_id: int) -> PantryStatsResponse:
        stats = await self.pantry_service.get_pantry_stats(user_id)
        return stats.to_schema()

    async def list_expiring_items(self, user_id: int) -> List[PantryItemResponse]:
        items = await self.pantry_service.get_expiring_items(user_id)
        return [item.to_schema() for item in items]
