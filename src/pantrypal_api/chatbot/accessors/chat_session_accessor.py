from typing import List

from injector import inject
from sqlalchemy.future import select

from src.core.chatbot.accessors.chat_session_accessor import IChatSessionAccessor
from src.core.chatbot.models import ChatSessionDomain
from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.chatbot.models import ChatSession


class ChatSessionAccessor(IChatSessionAccessor):
    """Accesses and stores user's chat sessions using DB provider."""

    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
        logging_provider: ILoggingProvider,
    ):
        self.db_provider = db_provider
        self.logging_provider = logging_provider

    async def list_sessions(self, user_id: int) -> List[ChatSessionDomain]:
        async with self.db_provider.get_db() as session:
            result = await session.execute(
                select(ChatSession)
                .where(ChatSession.user_id == user_id)
                .where(ChatSession.deleted_at.is_(None))
            )
            records = result.scalars().all()
            return [r.to_domain() for r in records]

    async def create_session(
        self, session_domain: ChatSessionDomain
    ) -> ChatSessionDomain:
        record = ChatSession(
            user_id=session_domain.user_id,
            title=session_domain.title,
            summary=session_domain.summary,
            prep_time=session_domain.prep_time,
            instructions="|".join(session_domain.instructions),
            ingredients="|".join(session_domain.ingredients),
            available_count=session_domain.available_ingredients,
            total_count=session_domain.total_ingredients,
        )
        async with self.db_provider.get_db() as db:
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return record.to_domain()

    async def update_session_recipe(
        self, session_id: int, session_domain: ChatSessionDomain
    ) -> ChatSessionDomain:
        async with self.db_provider.get_db() as db:
            record = await db.get(ChatSession, session_id)
            if record is None:
                raise ValueError("Session not found")
            if record.deleted_at is not None:
                raise ValueError("Session deleted")

            record.title = session_domain.title
            record.summary = session_domain.summary
            record.prep_time = session_domain.prep_time
            record.instructions = "|".join(session_domain.instructions)
            record.ingredients = "|".join(session_domain.ingredients)
            record.available_count = session_domain.available_ingredients
            record.total_count = session_domain.total_ingredients

            await db.commit()
            await db.refresh(record)
            return record.to_domain()

    async def soft_delete_session(self, session_id: int) -> None:
        async with self.db_provider.get_db() as db:
            record = await db.get(ChatSession, session_id)
            if record is None:
                return
            if record.deleted_at is None:
                record.deleted_at = DateTimeUtils.get_utc_now()
            await db.commit()
