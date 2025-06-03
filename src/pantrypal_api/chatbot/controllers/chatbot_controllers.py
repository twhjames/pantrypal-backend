from injector import inject

from src.core.chatbot.services.chatbot_service import ChatbotService
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import ChatReply, Message


class ChatbotController:
    @inject
    def __init__(
        self,
        chatbot_service: ChatbotService,
    ):
        self.chatbot_service = chatbot_service

    async def get_recipe_recommendation(self, message: Message) -> ChatReply:
        spec = message.to_spec()
        reply = await self.chatbot_service.get_first_recommendation(spec)
        return ChatReply(reply=reply)

    async def get_contextual_chat_reply(self, message: Message) -> ChatReply:
        spec = message.to_spec()
        reply = await self.chatbot_service.chat_with_context(spec)
        return ChatReply(reply=reply)
