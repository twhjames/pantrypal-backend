from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from src.core.pantry.models import Category, Unit


class AddPantryItemSpec(BaseModel):
    item_name: str
    quantity: float
    unit: Unit
    category: Optional[Category] = None
    expiry_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None


class UpdatePantryItemSpec(BaseModel):
    id: int
    item_name: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[Unit] = None
    category: Optional[Category] = None
    expiry_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None


class DeletePantryItemsSpec(BaseModel):
    item_ids: List[int]
