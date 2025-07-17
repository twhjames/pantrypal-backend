from typing import List

from injector import inject

from src.core.chatbot.services.chat_session_service import ChatSessionService
from src.pantrypal_api.chatbot.schemas.chat_session_schemas import ChatSessionResponse
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import Message


class ChatSessionController:
    @inject
    def __init__(self, chat_session_service: ChatSessionService):
        self.chat_session_service = chat_session_service

    async def list_sessions(self, user_id: int) -> List[ChatSessionResponse]:
        """Return session summaries for a user."""
        sessions = await self.chat_session_service.list_sessions(user_id)
        return [s.to_schema() for s in sessions]

    async def get_history(self, session_id: int) -> List[Message]:
        """Retrieve the message log for a chat session."""
        history = await self.chat_session_service.get_session_history(session_id)
        return [h.to_schema() for h in history]

    async def delete_session(self, session_id: int) -> None:
        """Soft delete a chat session and its history."""
        await self.chat_session_service.delete_session(session_id)
