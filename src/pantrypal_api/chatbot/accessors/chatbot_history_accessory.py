from typing import List

from injector import inject
from sqlalchemy.future import select

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.models import ChatHistoryDomain
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.common.utils import DateTimeUtils
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.chatbot.models import ChatHistory


class ChatbotHistoryAccessor(IChatbotHistoryAccessor):
    """Accesses and stores chatbot history using DB provider."""

    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
        secret_provider: ISecretProvider,
    ):
        self.db_provider = db_provider
        self.secret_provider = secret_provider

    async def save_message(self, message: ChatMessageSpec) -> None:
        async with self.db_provider.get_db() as session:
            chat_history_entry = self.__to_model(message)
            session.add(chat_history_entry)
            await session.commit()

    async def get_recent_messages(self, user_id: int) -> List[ChatHistoryDomain]:
        limit = self.__get_max_chat_history()
        async with self.db_provider.get_db() as session:
            result = await session.execute(
                select(ChatHistory)
                .where(ChatHistory.user_id == user_id)
                .order_by(ChatHistory.created_at.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
        return [msg.to_domain() for msg in reversed(messages)]

    def __get_max_chat_history(self) -> int:
        return int(self.secret_provider.get_secret(SecretKey.CHATBOT_MAX_CHAT_HISTORY))

    def __to_model(self, spec: ChatMessageSpec) -> ChatHistory:
        return ChatHistory(
            user_id=spec.user_id,
            role=spec.role,
            content=spec.content,
            timestamp=spec.timestamp or DateTimeUtils.get_utc_now(),
        )
