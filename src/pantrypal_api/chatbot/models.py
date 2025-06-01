from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import Integer, Text

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.models import ChatHistoryDomain
from src.pantrypal_api.base.models import PantryPalBaseModel
from src.pantrypal_api.common.utils import TimeUtils


class ChatHistory(PantryPalBaseModel):
    __tablename__ = "chat_history"

    user_id = Column(Integer, index=True)
    role = Column(
        SQLAEnum(
            ChatbotMessageRole,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False,
        ),
        nullable=False,
    )
    content = Column(Text)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, default=lambda: TimeUtils.get_utc_now()
    )

    def to_domain(self) -> ChatHistoryDomain:
        return ChatHistoryDomain(
            id=self.id,
            created_at=self.created_at,
            user_id=self.user_id,
            role=self.role,
            content=self.content,
            timestamp=self.timestamp,
        )
