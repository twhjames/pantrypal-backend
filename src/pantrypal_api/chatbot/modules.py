from injector import Binder, Module, singleton

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.pantrypal_api.chatbot.adapters.chatbot_provider import GroqChatbotProvider


class ChatbotModule(Module):
    def configure(self, binder: Binder):
        binder.bind(IChatbotProvider, to=GroqChatbotProvider, scope=singleton)
