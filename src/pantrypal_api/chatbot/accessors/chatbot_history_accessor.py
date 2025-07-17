from typing import List, Optional

from injector import inject
from sqlalchemy import update
from sqlalchemy.future import select

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.chatbot.models import ChatHistory


class ChatbotHistoryAccessor(IChatbotHistoryAccessor):
    """Accesses and stores chatbot history using DB provider."""

    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
        secret_provider: ISecretProvider,
        logging_provider: ILoggingProvider,
    ):
        self.db_provider = db_provider
        self.secret_provider = secret_provider
        self.logging_provider = logging_provider

    async def save_message(self, message: ChatMessageSpec) -> None:
        try:
            async with self.db_provider.get_db() as session:
                chat_history_entry = self.__to_model(message)
                session.add(chat_history_entry)
                await session.commit()
        except Exception as e:
            self.logging_provider.error(
                "Failed to save chatbot message",
                extra_data={
                    "user_id": message.user_id,
                    "role": message.role.name,
                    "error": str(e),
                },
                tag="ChatbotHistoryAccessor",
            )
            raise

    async def get_recent_messages(
        self, user_id: int, session_id: Optional[int] = None
    ) -> List[ChatHistoryDomain]:
        try:
            limit = self.__get_max_chat_history()
            async with self.db_provider.get_db() as session:
                stmt = (
                    select(ChatHistory)
                    .where(ChatHistory.user_id == user_id)
                    .where(ChatHistory.deleted_at.is_(None))
                    .order_by(ChatHistory.created_at.desc())
                    .limit(limit)
                )
                if session_id is not None:
                    stmt = stmt.where(ChatHistory.session_id == session_id)
                result = await session.execute(stmt)
                messages = result.scalars().all()
            return [msg.to_domain() for msg in reversed(messages)]
        except Exception as e:
            self.logging_provider.error(
                "Failed to fetch chatbot history",
                extra_data={"user_id": user_id, "error": str(e)},
                tag="ChatbotHistoryAccessor",
            )
            raise

    async def get_messages_by_session(self, session_id: int) -> List[ChatHistoryDomain]:
        try:
            async with self.db_provider.get_db() as session:
                result = await session.execute(
                    select(ChatHistory)
                    .where(ChatHistory.session_id == session_id)
                    .where(ChatHistory.deleted_at.is_(None))
                    .order_by(ChatHistory.created_at.asc())
                )
                messages = result.scalars().all()
            return [msg.to_domain() for msg in messages]
        except Exception as e:
            self.logging_provider.error(
                "Failed to fetch chatbot history by session",
                extra_data={"session_id": session_id, "error": str(e)},
                tag="ChatbotHistoryAccessor",
            )
            raise

    async def soft_delete_history_by_session(self, session_id: int) -> None:
        async with self.db_provider.get_db() as session:
            await session.execute(
                update(ChatHistory)
                .where(ChatHistory.session_id == session_id)
                .where(ChatHistory.deleted_at.is_(None))
                .values(deleted_at=DateTimeUtils.get_utc_now())
            )
            await session.commit()

    def __get_max_chat_history(self) -> int:
        return int(self.secret_provider.get_secret(SecretKey.CHATBOT_MAX_CHAT_HISTORY))

    def __to_model(self, spec: ChatMessageSpec) -> ChatHistory:
        return ChatHistory(
            user_id=spec.user_id,
            session_id=spec.session_id,
            role=spec.role,
            content=spec.content,
            timestamp=spec.timestamp or DateTimeUtils.get_utc_now(),
        )
