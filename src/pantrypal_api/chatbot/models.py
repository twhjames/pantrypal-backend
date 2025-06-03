from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import Integer, Text

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.models import ChatHistoryDomain
from src.core.common.utils import DateTimeUtils
from src.pantrypal_api.base.models import PantryPalBaseModel


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
        DateTime(timezone=True),
        nullable=False,
        default=lambda: DateTimeUtils.get_utc_now(),
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
