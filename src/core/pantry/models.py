from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.core.base.models import PantryPalMutableModelDomain
from src.core.common.utils import DateTimeUtils
from src.core.pantry.constants import Category, Unit
from src.pantrypal_api.pantry.schemas.pantry_schemas import (
    PantryItemResponse,
    PantryStatsResponse,
)


class PantryItemDomain(PantryPalMutableModelDomain):
    user_id: int
    item_name: str
    quantity: float
    unit: Unit
    category: Optional[Category] = None
    purchase_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    def to_schema(self) -> PantryItemResponse:
        return PantryItemResponse(
            id=self.id,
            user_id=self.user_id,
            item_name=self.item_name,
            quantity=self.quantity,
            unit=self.unit,
            category=self.category,
            purchase_date=self.purchase_date,
            expiry_date=self.expiry_date,
        )

    @classmethod
    def create(
        cls,
        user_id: int,
        item_name: str,
        quantity: float,
        unit: Unit,
        category: Optional[Category] = None,
        purchase_date: Optional[datetime] = None,
        expiry_date: Optional[datetime] = None,
    ) -> "PantryItemDomain":
        now = DateTimeUtils.get_utc_now()
        return cls(
            id=0,  # placeholder before DB insert
            user_id=user_id,
            item_name=item_name,
            quantity=quantity,
            unit=unit,
            category=category,
            purchase_date=purchase_date,
            expiry_date=expiry_date,
            created_at=now,
            updated_at=now,
        )


class PantryStatsDomain(BaseModel):
    total_items: int
    expiring_soon: int
    expiring_today: int
    expired: int

    def to_schema(self) -> "PantryStatsResponse":
        return PantryStatsResponse(
            total=self.total_items,
            expiring_soon=self.expiring_soon,
            expiring_today=self.expiring_today,
            expired=self.expired,
        )
