from typing import Dict, List

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider


class ChatbotService:
    def __init__(self, chatbot_provider: IChatbotProvider):
        self.chatbot_provider = chatbot_provider

    async def get_first_recommendation(self, message: str) -> str:
        return await self.chatbot_provider.generate_first_reply(message)

    async def chat_with_context(self, messages: List[Dict[str, str]]) -> str:
        return await self.chatbot_provider.generate_reply(messages)
