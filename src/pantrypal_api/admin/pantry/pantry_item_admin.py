from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.pantry.models import PantryItem


class PantryItemAdmin(PantryPalModelAdmin, model=PantryItem):
    name = "Pantry Item"
    name_plural = "Pantry Items"
    icon = "fa-solid fa-utensils"

    column_list = [
        PantryItem.id,
        PantryItem.user_id,
        PantryItem.item_name,
        PantryItem.quantity,
        PantryItem.unit,
        PantryItem.category,
        PantryItem.purchase_date,
        PantryItem.expiry_date,
        PantryItem.created_at,
        PantryItem.updated_at,
    ]

    form_columns = [
        PantryItem.user_id,
        PantryItem.item_name,
        PantryItem.quantity,
        PantryItem.unit,
        PantryItem.category,
        PantryItem.purchase_date,
        PantryItem.expiry_date,
    ]

    column_searchable_list = [
        PantryItem.item_name,
        PantryItem.category,
        PantryItem.user_id,
    ]

    column_filters = [
        PantryItem.unit,
        PantryItem.category,
    ]
