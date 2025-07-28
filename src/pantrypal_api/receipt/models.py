from sqlalchemy import JSON, Column, Integer, String

from src.core.receipt.models import ReceiptResultDomain
from src.pantrypal_api.base.models import PantryPalBaseModel


class ReceiptResult(PantryPalBaseModel):
    __tablename__ = "receipt_result"

    user_id = Column(Integer, index=True)
    receipt_id = Column(String, unique=True)
    result = Column(JSON)

    def to_domain(self) -> ReceiptResultDomain:
        return ReceiptResultDomain(
            id=self.id,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
            user_id=self.user_id,
            receipt_id=self.receipt_id,
            result=self.result,
        )
