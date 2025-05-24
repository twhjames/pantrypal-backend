from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import date

router = APIRouter()

# Pydantic model
class PantryItem(BaseModel):
    name: str
    quantity: int
    purchase_date: date
    predicted_expiry: date

# In-memory storage (for demo)
pantry_items: List[PantryItem] = []

@router.get("/items", response_model=List[PantryItem])
def get_items():
    return pantry_items

@router.post("/items")
def add_item(item: PantryItem):
    pantry_items.append(item)
    return {"message": "Item added", "item": item}
