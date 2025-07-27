from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.receipt.models import ReceiptResult


class ReceiptResultAdmin(PantryPalModelAdmin, model=ReceiptResult):
    """Admin view for processed receipt results."""

    name = "Receipt Result"
    name_plural = "Receipt Results"
    icon = "fa-solid fa-receipt"

    column_list = [
        ReceiptResult.id,
        ReceiptResult.user_id,
        ReceiptResult.receipt_id,
        ReceiptResult.result,
        ReceiptResult.created_at,
        ReceiptResult.updated_at,
    ]

    form_columns = [
        ReceiptResult.user_id,
        ReceiptResult.receipt_id,
        ReceiptResult.result,
    ]
