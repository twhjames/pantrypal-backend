from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.chatbot.models import ChatSession


class ChatSessionAdmin(PantryPalModelAdmin, model=ChatSession):
    name = "Chat Session"
    name_plural = "Chat Sessions"
    icon = "fa-solid fa-comments"

    column_list = [
        ChatSession.id,
        ChatSession.user_id,
        ChatSession.title,
        ChatSession.summary,
        ChatSession.prep_time,
        ChatSession.available_count,
        ChatSession.total_count,
        ChatSession.created_at,
        ChatSession.deleted_at,
        ChatSession.updated_at,
    ]

    form_columns = [
        ChatSession.user_id,
        ChatSession.title,
        ChatSession.summary,
        ChatSession.prep_time,
        ChatSession.instructions,
        ChatSession.ingredients,
        ChatSession.available_count,
        ChatSession.total_count,
    ]

    column_searchable_list = [ChatSession.title, ChatSession.summary]
    column_sortable_list = [ChatSession.created_at]
