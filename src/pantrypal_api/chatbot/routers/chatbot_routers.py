from fastapi import APIRouter, Depends

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.pantrypal_api.chatbot.controllers.chatbot_controllers import ChatbotController
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import ChatReply, Message
from src.pantrypal_api.modules import injector

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# Dependency factory function for controller
def get_chatbot_controller() -> ChatbotController:
    chatbot_provider = injector.get(IChatbotProvider)
    chat_history_accessor = injector.get(IChatbotHistoryAccessor)
    return ChatbotController(chatbot_provider, chat_history_accessor)


@router.post(
    "/recommend",
    response_model=ChatReply,
    summary="Get a one-shot recipe recommendation",
    description="Send a single message to receive a quick recipe recommendation from PantryPal Assistant.",
)
async def recommend_recipe(
    message: Message, controller: ChatbotController = Depends(get_chatbot_controller)
):
    reply = await controller.get_recipe_recommendation(message)
    return ChatReply(reply=reply)


@router.post(
    "/chat",
    response_model=ChatReply,
    summary="Chat with PantryPal Assistant (conversational)",
    description="Send a series of chat messages to receive a contextual reply from PantryPal Assistant.",
)
async def chat_with_history(
    message: Message, controller: ChatbotController = Depends(get_chatbot_controller)
):
    reply = await controller.get_contextual_chat_reply(message)
    return ChatReply(reply=reply)
