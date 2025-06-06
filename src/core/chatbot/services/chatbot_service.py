from datetime import datetime

from injector import inject

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider


class ChatbotService:
    """
    Service layer for managing chatbot interactions.

    Bridges the chatbot provider and message history accessor to handle:
    - One-shot recipe recommendations
    - Contextual conversations with history persistence
    """

    @inject
    def __init__(
        self,
        chatbot_provider: IChatbotProvider,
        chat_history_accessor: IChatbotHistoryAccessor,
        logging_provider: ILoggingProvider,
    ):
        """
        Initializes the chatbot service with the given provider and chat history accessor.

        :param chatbot_provider: Interface to the LLM provider
        :param chat_history_accessor: Interface to persist and retrieve message history
        """
        self.chatbot_provider = chatbot_provider
        self.chat_history_accessor = chat_history_accessor
        self.logging_provider = logging_provider

    async def get_first_recommendation(self, message: ChatMessageSpec) -> str:
        """
        Sends a one-shot message to the LLM without using chat history.

        :param message: The user's input message
        :return: The assistant's response string
        """
        self.logging_provider.info(
            f"Received one-shot message from user_id={message.user_id}"
        )
        try:
            reply = await self.chatbot_provider.handle_single_turn(message)
            self.logging_provider.debug(
                "LLM reply generated for one-shot recommendation"
            )
            return reply
        except Exception as e:
            self.logging_provider.error(f"Error in get_first_recommendation: {str(e)}")
            raise

    async def chat_with_context(self, message: ChatMessageSpec) -> str:
        """
        Handles a complete chat flow by storing the user message, retrieving message history,
        sending context to the LLM, and saving the assistant's reply.

        :param message: The latest user message
        :return: The assistant's response string
        """
        self.logging_provider.info(
            f"Processing contextual message for user_id={message.user_id}"
        )
        try:
            await self.chat_history_accessor.save_message(message)
            self.logging_provider.debug("User message saved to chat history")

            recent_messages = await self.chat_history_accessor.get_recent_messages(
                message.user_id
            )
            self.logging_provider.debug(
                f"Fetched {len(recent_messages)} recent messages"
            )

            reply = await self.chatbot_provider.handle_multi_turn(recent_messages)
            self.logging_provider.debug("LLM reply generated for contextual chat")

            reply_timestamp = DateTimeUtils.get_utc_now()
            assistant_message = self.__create_chat_message_spec(
                user_id=message.user_id,
                role=ChatbotMessageRole.ASSISTANT,
                content=reply,
                timestamp=reply_timestamp,
            )
            await self.chat_history_accessor.save_message(assistant_message)
            self.logging_provider.debug("Assistant message saved to chat history")

            return reply
        except Exception as e:
            self.logging_provider.error(f"Error in chat_with_context: {str(e)}")
            raise

    def __create_chat_message_spec(
        self, user_id: int, role: ChatbotMessageRole, content: str, timestamp: datetime
    ) -> ChatMessageSpec:
        """
        Helper to constructs a ChatMessageSpec from components.

        :param user_id: User's ID
        :param role: Sender's role
        :param content: Message text
        :param timestamp: Timestamp of message creation
        :return: ChatMessageSpec
        """
        return ChatMessageSpec(
            user_id=user_id, role=role, content=content, timestamp=timestamp
        )
