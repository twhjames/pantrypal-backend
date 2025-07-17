from abc import ABC, abstractmethod
from typing import List

from src.core.chatbot.models import ChatSessionDomain


class IChatSessionAccessor(ABC):
    """Data access layer for chat sessions."""

    @abstractmethod
    async def list_sessions(self, user_id: int) -> List[ChatSessionDomain]:
        """Return all sessions for a user."""
        raise NotImplementedError

    @abstractmethod
    async def create_session(self, session: ChatSessionDomain) -> ChatSessionDomain:
        """Create a new chat session."""
        raise NotImplementedError

    @abstractmethod
    async def update_session_recipe(
        self, session_id: int, session: ChatSessionDomain
    ) -> ChatSessionDomain:
        """Update stored recipe details for a session."""
        raise NotImplementedError

    @abstractmethod
    async def soft_delete_session(self, session_id: int) -> None:
        """Soft delete a chat session."""
        raise NotImplementedError
