from typing import Any, Dict

from src.core.base.models import PantryPalBaseModelDomain
from src.core.common.utils import DateTimeUtils


class ReceiptResultDomain(PantryPalBaseModelDomain):
    user_id: int
    receipt_id: str
    result: Dict[str, Any]

    @classmethod
    def create(
        cls,
        user_id: int,
        receipt_id: str,
        result: Dict[str, Any],
    ) -> "ReceiptResultDomain":
        return cls(
            id=0,
            user_id=user_id,
            receipt_id=receipt_id,
            result=result,
            created_at=DateTimeUtils.get_utc_now(),
            deleted_at=None,
        )
