from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.configuration.models import Configuration


class ConfigurationAdmin(PantryPalModelAdmin, model=Configuration):
    column_list = [
        Configuration.key,
        Configuration.value,
        Configuration.description,
    ]
    form_columns = [
        Configuration.key,
        Configuration.value,
        Configuration.description,
    ]
    column_searchable_list = [Configuration.key, Configuration.description]
    column_sortable_list = [Configuration.key]
    name = "Configuration"
    name_plural = "Configurations"
