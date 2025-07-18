from injector import inject

from src.core.chatbot.services.chatbot_service import ChatbotService
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import (
    ChatReply,
    ContextualChatMessage,
    RecommendMessage,
    TitleSuggestions,
)


class ChatbotController:
    @inject
    def __init__(
        self,
        chatbot_service: ChatbotService,
    ):
        self.chatbot_service = chatbot_service

    async def get_recipe_recommendation(
        self, user_id: int, message: RecommendMessage
    ) -> ChatReply:
        spec = message.to_spec(user_id)
        reply, session_id = await self.chatbot_service.get_first_recommendation(spec)
        return ChatReply(reply=reply, session_id=session_id)

    async def get_contextual_chat_reply(
        self, user_id: int, message: ContextualChatMessage
    ) -> ChatReply:
        spec = message.to_spec(user_id)
        reply = await self.chatbot_service.chat_with_context(spec)
        return ChatReply(reply=reply)

    async def get_recipe_title_suggestions(self, user_id: int) -> TitleSuggestions:
        suggestions = await self.chatbot_service.get_recipe_title_suggestions(user_id)
        return TitleSuggestions(suggestions=suggestions)
