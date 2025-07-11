from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.core.chatbot.constants import ChatbotMessageRole


class ChatMessageSpec(BaseModel):
    user_id: int
    role: ChatbotMessageRole
    content: str
    timestamp: datetime
    session_id: Optional[int] = None
