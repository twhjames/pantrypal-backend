from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import Integer, String, Text

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.models import ChatHistoryDomain, ChatSessionDomain
from src.core.common.utils import DateTimeUtils
from src.pantrypal_api.base.models import PantryPalBaseModel


class ChatHistory(PantryPalBaseModel):
    __tablename__ = "chat_history"

    user_id = Column(Integer, index=True)
    session_id = Column(Integer, index=True, nullable=True)
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
            deleted_at=self.deleted_at,
            user_id=self.user_id,
            role=self.role,
            content=self.content,
            timestamp=self.timestamp,
            session_id=self.session_id,
        )


class ChatSession(PantryPalBaseModel):
    __tablename__ = "chat_session"

    user_id = Column(Integer, index=True)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=True)
    prep_time = Column(Integer, nullable=True)
    instructions = Column(Text, nullable=True)
    ingredients = Column(Text, nullable=True)
    available_count = Column(Integer, nullable=True)
    total_count = Column(Integer, nullable=True)

    def to_domain(self) -> ChatSessionDomain:
        return ChatSessionDomain(
            id=self.id,
            created_at=self.created_at,
            deleted_at=self.deleted_at,
            user_id=self.user_id,
            title=self.title,
            summary=self.summary,
            prep_time=self.prep_time,
            instructions=self.instructions.split("|") if self.instructions else [],
            ingredients=self.ingredients.split("|") if self.ingredients else [],
            available_ingredients=self.available_count or 0,
            total_ingredients=self.total_count or 0,
            updated_at=self.updated_at,
        )
