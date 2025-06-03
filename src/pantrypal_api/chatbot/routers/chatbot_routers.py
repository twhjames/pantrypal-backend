from fastapi import APIRouter, Depends

from src.core.chatbot.services.chatbot_service import ChatbotService
from src.pantrypal_api.chatbot.controllers.chatbot_controllers import ChatbotController
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import ChatReply, Message
from src.pantrypal_api.modules import injector

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# Dependency factory function for controller with injected services
def get_chatbot_controller() -> ChatbotController:
    chatbot_service = injector.get(ChatbotService)
    return ChatbotController(chatbot_service)


@router.post(
    "/recommend",
    response_model=ChatReply,
    summary="Get a one-shot recipe recommendation",
    description="Send a single message to receive a quick recipe recommendation from PantryPal Assistant.",
)
async def recommend_recipe(
    message: Message, controller: ChatbotController = Depends(get_chatbot_controller)
):
    return await controller.get_recipe_recommendation(message)


@router.post(
    "/chat",
    response_model=ChatReply,
    summary="Chat with PantryPal Assistant (conversational)",
    description="Send a series of chat messages to receive a contextual reply from PantryPal Assistant.",
)
async def chat_with_history(
    message: Message, controller: ChatbotController = Depends(get_chatbot_controller)
):
    return await controller.get_contextual_chat_reply(message)
