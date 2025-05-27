from abc import ABC, abstractmethod
from typing import Dict, List


class IChatbotProvider(ABC):
    @abstractmethod
    async def generate_first_reply(self, message: str) -> str:
        pass

    @abstractmethod
    async def generate_reply(self, messages: List[Dict[str, str]]) -> str:
        pass
