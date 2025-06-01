from dataclasses import dataclass
from datetime import datetime

from src.core.chatbot.constants import ChatbotMessageRole


@dataclass
class ChatMessageSpec:
    user_id: int
    role: ChatbotMessageRole
    content: str
    timestamp: datetime
