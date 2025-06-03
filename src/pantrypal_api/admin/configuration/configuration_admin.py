from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.configuration.models import Configuration


class ConfigurationAdmin(PantryPalModelAdmin, model=Configuration):
    name = "Configuration"
    name_plural = "Configurations"
    icon = "fa-solid fa-gears"

    column_list = [
        Configuration.id,
        Configuration.key,
        Configuration.value,
        Configuration.description,
        Configuration.created_at,
        Configuration.updated_at,
    ]

    form_columns = [
        Configuration.key,
        Configuration.value,
        Configuration.description,
    ]

    column_searchable_list = [
        Configuration.key,
        Configuration.description,
    ]

    column_sortable_list = [
        Configuration.key,
    ]
