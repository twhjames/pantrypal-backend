from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin
from src.pantrypal_api.chatbot.models import ChatHistory


class ChatHistoryAdmin(PantryPalModelAdmin, model=ChatHistory):
    column_list = [
        ChatHistory.id,
        ChatHistory.user_id,
        ChatHistory.role,
        ChatHistory.content,
        ChatHistory.timestamp,
    ]
    form_columns = [
        ChatHistory.user_id,
        ChatHistory.role,
        ChatHistory.content,
    ]
    column_searchable_list = [ChatHistory.content, ChatHistory.role]
    column_sortable_list = [ChatHistory.timestamp]
    name = "Chat History"
    name_plural = "Chat Histories"
