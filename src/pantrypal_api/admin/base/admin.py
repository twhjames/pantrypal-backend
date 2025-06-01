from sqladmin import ModelView


class PantryPalModelAdmin(ModelView):
    """
    Base admin class for PantryPal models.
    Shared behavior and UI config for all admin views can go here.
    """

    page_size = 20
    can_export = True
    name_plural = "Records"
    icon = "fa-solid fa-database"

    # Add custom labels
    column_labels = {}

    column_sortable_list = ["id"]
    column_searchable_list = ["id"]
    form_excluded_columns = []  # Nothing to exclude now

    # Add common methods or overrides if needed
