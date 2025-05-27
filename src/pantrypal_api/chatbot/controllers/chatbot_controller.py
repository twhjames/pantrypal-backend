from typing import Dict, List

from injector import inject

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.services.chatbot_service import ChatbotService


class ChatbotController:
    @inject
    def __init__(self, chatbot_provider: IChatbotProvider):
        self.chatbot_service = ChatbotService(chatbot_provider)

    async def generate_first_cut_reply(self, message: str) -> str:
        return await self.chatbot_service.get_first_recommendation(message)

    async def generate_reply_with_context(self, messages: List[Dict[str, str]]) -> str:
        return await self.chatbot_service.chat_with_context(messages)
