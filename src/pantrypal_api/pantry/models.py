from sqlalchemy import Column, DateTime, Enum, Float, Integer, String

from src.core.pantry.constants import Category, Unit
from src.core.pantry.models import PantryItemDomain
from src.pantrypal_api.base.models import PantryPalBaseModel


class PantryItem(PantryPalBaseModel):
    __tablename__ = "pantry_item"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    item_name = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(Enum(Unit), nullable=False)
    category = Column(Enum(Category), nullable=False)
    purchase_date = Column(DateTime, nullable=True)
    expiry_date = Column(DateTime, nullable=True)

    def to_domain(self) -> PantryItemDomain:
        return PantryItemDomain(
            id=self.id,
            user_id=self.user_id,
            item_name=self.item_name,
            quantity=self.quantity,
            unit=self.unit,
            category=self.category,
            purchase_date=self.purchase_date,
            expiry_date=self.expiry_date,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
