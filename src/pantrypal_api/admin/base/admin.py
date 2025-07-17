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

    # Common searchable and sortable fields
    column_sortable_list = ["id", "created_at", "updated_at", "deleted_at"]
    column_searchable_list = ["id"]

    # Exclude these from form by default
    form_excluded_columns = ["id", "created_at", "updated_at", "deleted_at"]

    # Optional: add labels for readability
    column_labels = {
        "created_at": "Created At",
        "updated_at": "Updated At",
        "deleted_at": "Deleted At",
    }

    # Default sort: newest first
    column_default_sort = ("created_at", True)
