from injector import Binder, Module, singleton

from src.core.chatbot.accessors.chat_session_accessor import IChatSessionAccessor
from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.pantrypal_api.chatbot.accessors.chat_session_accessor import (
    ChatSessionAccessor,
)
from src.pantrypal_api.chatbot.accessors.chatbot_history_accessor import (
    ChatbotHistoryAccessor,
)
from src.pantrypal_api.chatbot.adapters.chatbot_provider import GroqChatbotProvider


class ChatbotModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IChatbotProvider, to=GroqChatbotProvider, scope=singleton)
        binder.bind(IChatbotHistoryAccessor, to=ChatbotHistoryAccessor, scope=singleton)
        binder.bind(IChatSessionAccessor, to=ChatSessionAccessor, scope=singleton)
