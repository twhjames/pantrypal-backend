from typing import List

from fastapi import APIRouter, Depends, Query

from src.core.chatbot.services.chat_session_service import ChatSessionService
from src.core.chatbot.services.chatbot_service import ChatbotService
from src.pantrypal_api.chatbot.controllers.chat_session_controllers import (
    ChatSessionController,
)
from src.pantrypal_api.chatbot.controllers.chatbot_controllers import ChatbotController
from src.pantrypal_api.chatbot.schemas.chat_session_schemas import ChatSessionResponse
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import (
    ChatReply,
    ContextualChatMessage,
    Message,
    RecommendMessage,
)
from src.pantrypal_api.modules import injector

router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


# Dependency factory function for controller with injected services
def get_chatbot_controller() -> ChatbotController:
    chatbot_service = injector.get(ChatbotService)
    return ChatbotController(chatbot_service)


def get_chat_session_controller() -> ChatSessionController:
    chat_session_service = injector.get(ChatSessionService)
    return ChatSessionController(chat_session_service)


@router.post(
    "/recommend",
    response_model=ChatReply,
    summary="Get a one-shot recipe recommendation",
    description="Send a single message to receive a quick recipe recommendation from PantryPal Assistant.",
)
async def recommend_recipe(
    message: RecommendMessage,
    controller: ChatbotController = Depends(get_chatbot_controller),
):
    return await controller.get_recipe_recommendation(message)


@router.post(
    "/chat",
    response_model=ChatReply,
    summary="Chat with PantryPal Assistant (conversational)",
    description="Send a series of chat messages to receive a contextual reply from PantryPal Assistant.",
)
async def chat_with_history(
    message: ContextualChatMessage,
    controller: ChatbotController = Depends(get_chatbot_controller),
):
    return await controller.get_contextual_chat_reply(message)


@router.get(
    "/sessions",
    response_model=List[ChatSessionResponse],
    summary="List chat sessions for user",
)
async def list_sessions(
    user_id: int = Query(..., description="User ID"),
    controller: ChatSessionController = Depends(get_chat_session_controller),
):
    return await controller.list_sessions(user_id)


@router.get(
    "/sessions/{session_id}",
    response_model=List[Message],
    summary="Get chat history for session",
)
async def get_session_history(
    session_id: int,
    controller: ChatSessionController = Depends(get_chat_session_controller),
):
    return await controller.get_history(session_id)


@router.delete(
    "/sessions/{session_id}",
    status_code=204,
    summary="Delete chat session",
)
async def delete_session(
    session_id: int,
    controller: ChatSessionController = Depends(get_chat_session_controller),
):
    await controller.delete_session(session_id)
