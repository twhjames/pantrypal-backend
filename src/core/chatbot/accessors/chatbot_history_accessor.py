from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.specs import ChatMessageSpec


class IChatbotHistoryAccessor(ABC):
    @abstractmethod
    async def save_message(self, message: ChatMessageSpec) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_recent_messages(
        self, user_id: int, session_id: Optional[int] = None
    ) -> List[ChatHistoryDomain]:
        raise NotImplementedError

    @abstractmethod
    async def get_messages_by_session(self, session_id: int) -> List[ChatHistoryDomain]:
        raise NotImplementedError

    @abstractmethod
    async def soft_delete_history_by_session(self, session_id: int) -> None:
        """Mark all history entries for a session as deleted."""
        raise NotImplementedError
