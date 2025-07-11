from datetime import datetime
from typing import List, Optional

from src.core.base.models import PantryPalBaseModelDomain
from src.core.chatbot.constants import ChatbotMessageRole
from src.pantrypal_api.chatbot.schemas.chat_session_schemas import ChatSessionResponse
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import Message


class ChatHistoryDomain(PantryPalBaseModelDomain):
    user_id: int
    role: ChatbotMessageRole
    content: str
    timestamp: datetime
    session_id: Optional[int] = None

    def to_schema(self) -> Message:
        return Message(
            id=self.id,
            user_id=self.user_id,
            role=self.role.value if hasattr(self.role, "value") else self.role,
            content=self.content,
            timestamp=self.timestamp,
            session_id=self.session_id,
        )

    @classmethod
    def create(
        cls,
        user_id: int,
        role: ChatbotMessageRole,
        content: str,
        timestamp: datetime,
        session_id: Optional[int] = None,
    ) -> "ChatHistoryDomain":
        return cls(
            id=0,  # placeholder before DB insert
            user_id=user_id,
            role=role,
            content=content,
            timestamp=timestamp,
            session_id=session_id,
        )


class ChatSessionDomain(PantryPalBaseModelDomain):
    user_id: int
    title: str
    summary: Optional[str] = None
    prep_time: Optional[int] = None
    instructions: List[str] = []
    ingredients: List[str] = []
    available_ingredients: int = 0
    total_ingredients: int = 0

    def to_schema(self) -> ChatSessionResponse:
        return ChatSessionResponse(
            id=self.id,
            title=self.title,
            summary=self.summary,
            prep_time=self.prep_time,
            instructions=self.instructions,
            ingredients=self.ingredients,
            available_ingredients=self.available_ingredients,
            total_ingredients=self.total_ingredients,
        )

    @classmethod
    def create(
        cls,
        user_id: int,
        title: str,
        summary: Optional[str] = None,
        prep_time: Optional[int] = None,
        instructions: Optional[List[str]] = None,
        ingredients: Optional[List[str]] = None,
        available_ingredients: int = 0,
        total_ingredients: int = 0,
    ) -> "ChatSessionDomain":
        return cls(
            id=0,  # placeholder before DB insert
            user_id=user_id,
            title=title,
            summary=summary,
            prep_time=prep_time,
            instructions=instructions or [],
            ingredients=ingredients or [],
            available_ingredients=available_ingredients,
            total_ingredients=total_ingredients,
        )
