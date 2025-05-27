from fastapi import APIRouter

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.pantrypal_api.chatbot.controllers.chatbot_controller import ChatbotController
from src.pantrypal_api.chatbot.schemas.chatbot_schema import (
    ChatPromptIn,
    ChatReplyOut,
    RecipePromptIn,
)
from src.pantrypal_api.modules import injector

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])

chatbot_provider = injector.get(IChatbotProvider)
controller = ChatbotController(chatbot_provider)


@router.post(
    "/recommend",
    response_model=ChatReplyOut,
    summary="Get first-cut recipe recommendation",
    description="Send a single prompt to get a one-shot recipe suggestion by PantryPal Chatbot.",
)
async def get_first_cut_recipe(prompt: RecipePromptIn):
    reply = await controller.generate_first_cut_reply(prompt.message)
    return ChatReplyOut(reply=reply)


@router.post(
    "/ask",
    response_model=ChatReplyOut,
    summary="Chat with PantryPal Assistant (conversational)",
    description="Sends a list of messages to support ongoing chat with history.",
)
async def chat_with_context(prompt: ChatPromptIn):
    reply = await controller.generate_reply_with_context(prompt.messages)
    return ChatReplyOut(reply=reply)
