from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import Integer, Text

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.models import ChatHistoryDomain
from src.pantrypal_api.base.models import PantryPalBaseModel
from src.pantrypal_api.common.utils import TimeUtils


class ChatHistory(PantryPalBaseModel):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    role = Column(SQLAEnum(ChatbotMessageRole), nullable=False)
    content = Column(Text)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, default=lambda: TimeUtils.get_utc_now()
    )

    def to_domain(self) -> ChatHistoryDomain:
        return ChatHistoryDomain(
            user_id=self.user_id,
            role=self.role,
            content=self.content,
            timestamp=self.timestamp,
        )
