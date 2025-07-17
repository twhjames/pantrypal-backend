from typing import List

from fastapi import APIRouter, Depends, status

from src.core.pantry.services.pantry_service import PantryService
from src.pantrypal_api.account.dependencies import get_current_user
from src.pantrypal_api.modules import injector
from src.pantrypal_api.pantry.controllers.pantry_controllers import PantryController
from src.pantrypal_api.pantry.schemas.pantry_schemas import (
    AddPantryItemRequest,
    DeletePantryItemsRequest,
    PantryItemResponse,
    UpdatePantryItemRequest,
)

router = APIRouter(prefix="/pantry", tags=["Pantry"])


def get_pantry_controller() -> PantryController:
    pantry_service = injector.get(PantryService)
    return PantryController(pantry_service=pantry_service)


@router.get("/list", response_model=List[PantryItemResponse])
async def list_pantry_items(
    controller: PantryController = Depends(get_pantry_controller),
    current_user_id: int = Depends(get_current_user),
):
    return await controller.get_items(current_user_id)


@router.post("/add", response_model=List[PantryItemResponse])
async def add_pantry_items(
    requests: List[AddPantryItemRequest],
    controller: PantryController = Depends(get_pantry_controller),
    current_user_id: int = Depends(get_current_user),
):
    return await controller.add_items(current_user_id, requests)


@router.patch("/update", response_model=PantryItemResponse)
async def update_pantry_item(
    request: UpdatePantryItemRequest,
    controller: PantryController = Depends(get_pantry_controller),
    current_user_id: int = Depends(get_current_user),
):
    return await controller.update_item(current_user_id, request)


@router.post("/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pantry_items(
    request: DeletePantryItemsRequest,
    controller: PantryController = Depends(get_pantry_controller),
    current_user_id: int = Depends(get_current_user),
):
    await controller.delete_items(current_user_id, request)
