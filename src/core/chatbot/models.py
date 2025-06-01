from datetime import datetime

from pydantic import BaseModel

from src.core.chatbot.constants import ChatbotMessageRole


class ChatHistoryDomain(BaseModel):
    user_id: int
    role: ChatbotMessageRole
    content: str
    timestamp: datetime
