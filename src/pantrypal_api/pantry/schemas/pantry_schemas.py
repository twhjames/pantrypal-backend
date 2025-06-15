from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, constr

from src.core.pantry.constants import Category, Unit
from src.core.pantry.specs import (
    AddPantryItemSpec,
    DeletePantryItemsSpec,
    UpdatePantryItemSpec,
)


class AddPantryItemRequest(BaseModel):
    item_name: constr(min_length=1)
    quantity: float
    unit: Unit
    category: Optional[Category] = None
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    def to_spec(self) -> AddPantryItemSpec:
        return AddPantryItemSpec(
            item_name=self.item_name,
            quantity=self.quantity,
            unit=self.unit,
            category=self.category,
            purchase_date=self.purchase_date,
            expiry_date=self.expiry_date,
        )


class UpdatePantryItemRequest(BaseModel):
    item_id: int
    item_name: Optional[constr(min_length=1)] = None
    quantity: Optional[float] = None
    unit: Optional[Unit] = None
    category: Optional[Category] = None
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    def to_spec(self) -> UpdatePantryItemSpec:
        return UpdatePantryItemSpec(
            id=self.item_id,
            item_name=self.item_name,
            quantity=self.quantity,
            unit=self.unit,
            category=self.category,
            purchase_date=self.purchase_date,
            expiry_date=self.expiry_date,
        )


class DeletePantryItemsRequest(BaseModel):
    item_ids: List[int]

    def to_spec(self) -> DeletePantryItemsSpec:
        return DeletePantryItemsSpec(
            item_ids=self.item_ids,
        )


class PantryItemResponse(BaseModel):
    id: int
    user_id: int
    item_name: str
    quantity: float
    unit: Unit
    category: Optional[Category]
    purchase_date: Optional[datetime]
    expiry_date: Optional[datetime]
