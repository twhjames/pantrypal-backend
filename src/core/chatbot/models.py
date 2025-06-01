from datetime import datetime

from src.core.base.models import PantryPalBaseModelDomain
from src.core.chatbot.constants import ChatbotMessageRole


class ChatHistoryDomain(PantryPalBaseModelDomain):
    user_id: int
    role: ChatbotMessageRole
    content: str
    timestamp: datetime
