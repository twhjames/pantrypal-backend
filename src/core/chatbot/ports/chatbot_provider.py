from abc import ABC, abstractmethod
from typing import List

from src.core.chatbot.specs import ChatMessageSpec


class IChatbotProvider(ABC):
    @abstractmethod
    async def handle_single_turn(self, message: ChatMessageSpec) -> str:
        """One-shot prompt processing without context"""
        raise NotImplementedError

    @abstractmethod
    async def handle_multi_turn(self, messages: List[ChatMessageSpec]) -> str:
        """Multi-turn conversation with history"""
        raise NotImplementedError
