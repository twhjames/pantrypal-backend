from typing import List

from injector import inject

from src.core.chatbot.accessors.chat_session_accessor import IChatSessionAccessor
from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.models import ChatHistoryDomain, ChatSessionDomain
from src.core.logging.ports.logging_provider import ILoggingProvider


class ChatSessionService:
    """Manage chat sessions and their stored recipe data."""

    @inject
    def __init__(
        self,
        chat_session_accessor: IChatSessionAccessor,
        chatbot_history_accessor: IChatbotHistoryAccessor,
        logging_provider: ILoggingProvider,
    ):
        self.chat_session_accessor = chat_session_accessor
        self.chatbot_history_accessor = chatbot_history_accessor
        self.logging_provider = logging_provider

    async def list_sessions(self, user_id: int) -> List[ChatSessionDomain]:
        """Return all sessions owned by a user."""
        return await self.chat_session_accessor.list_sessions(user_id)

    async def create_session(self, session: ChatSessionDomain) -> ChatSessionDomain:
        """Create and persist a new chat session."""
        return await self.chat_session_accessor.create_session(session)

    async def get_session_history(self, session_id: int) -> List[ChatHistoryDomain]:
        """Fetch full chat history for a session."""
        return await self.chatbot_history_accessor.get_messages_by_session(session_id)

    async def update_session_recipe(
        self, session_id: int, session: ChatSessionDomain
    ) -> ChatSessionDomain:
        """Persist updated recipe details for a session."""
        return await self.chat_session_accessor.update_session_recipe(
            session_id, session
        )

    async def delete_session(self, session_id: int) -> None:
        """Soft delete a chat session and its history."""
        await self.chat_session_accessor.soft_delete_session(session_id)
        await self.chatbot_history_accessor.soft_delete_history_by_session(session_id)
