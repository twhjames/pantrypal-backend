from abc import ABC, abstractmethod
from typing import List

from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.specs import ChatMessageSpec


class IChatbotHistoryAccessor(ABC):
    @abstractmethod
    async def save_message(self, message: ChatMessageSpec) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_recent_messages(self, user_id: int) -> List[ChatHistoryDomain]:
        raise NotImplementedError
