import json
import re
from datetime import datetime
from typing import List, Optional

from injector import inject

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.models import ChatSessionDomain
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.services.chat_session_service import ChatSessionService
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.pantry.services.pantry_service import PantryService


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
        pantry_service: PantryService,
        chat_session_service: ChatSessionService,
        chatbot_provider: IChatbotProvider,
        chatbot_history_accessor: IChatbotHistoryAccessor,
        logging_provider: ILoggingProvider,
    ):
        """
        Initializes the chatbot service with the given provider and chat history accessor.
        """
        self.pantry_service = pantry_service
        self.chat_session_service = chat_session_service
        self.chatbot_provider = chatbot_provider
        self.chatbot_history_accessor = chatbot_history_accessor
        self.logging_provider = logging_provider
        self._json_instruction = (
            "You are an assistant that recommends a recipe based on user-provided content.\n\n"
            "Respond strictly in JSON format with the following fields:\n"
            '- "title": (string) the recipe title\n'
            '- "summary": (string) a short description of the recipe\n'
            '- "prep_time": (string) total preparation time (e.g., "15 mins")\n'
            '- "ingredients": (list of strings) all required ingredients\n'
            '- "instructions": (ordered list of strings) step-by-step instructions\n'
            '- "available_ingredients": (list of strings) ingredients marked as available by the user\n'
            '- "total_ingredients": (integer) total number of unique ingredients\n'
            '- "assistant_comment": (string) your conversational response based on the message context. '
            "You may use markdown or formatting to enhance readability.\n\n"
            "Return only a valid JSON object, with no additional text before or after."
        )

    async def get_first_recommendation(
        self, message: ChatMessageSpec
    ) -> tuple[str, Optional[int]]:
        """
        Return the first recipe suggestion for a user.

        :param message: The user's input message
        :return: Tuple of the assistant's reply and the resolved session id
        """
        self.logging_provider.info(
            f"Received one-shot message from user_id={message.user_id}"
        )
        try:
            items = await self.pantry_service.get_items_sorted_by_expiry(
                message.user_id
            )
            if items:
                ingredient_list = ", ".join(
                    f"{i.item_name} {i.quantity} {i.unit} exp {i.expiry_date.date() if i.expiry_date else 'N/A'}"
                    for i in items
                )
                enriched = message.model_copy(
                    update={
                        "content": f"Prioritize ingredients nearing expiry: {ingredient_list}. "
                        + message.content
                    }
                )
            else:
                enriched = message

            messages = self.__prepend_format_instruction([enriched])
            reply = await self.chatbot_provider.handle_multi_turn(messages)
            self.logging_provider.debug("LLM reply generated for recipe recommendation")
            session_data = self.__parse_recipe_reply(reply, message.user_id)
            new_chat_session = await self.chat_session_service.create_session(
                session_data
            )

            user_message = message.model_copy(
                update={"session_id": new_chat_session.id}
            )

            await self.chatbot_history_accessor.save_message(user_message)
            self.logging_provider.debug("User message saved to chat history")

            reply_timestamp = DateTimeUtils.get_utc_now()
            assistant_message = self.__create_chat_message_spec(
                user_id=message.user_id,
                role=ChatbotMessageRole.ASSISTANT,
                content=reply,
                timestamp=reply_timestamp,
                session_id=new_chat_session.id,
            )
            await self.chatbot_history_accessor.save_message(assistant_message)
            self.logging_provider.debug("Assistant message saved to chat history")

            return reply, new_chat_session.id
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
            recent_messages = await self.chatbot_history_accessor.get_recent_messages(
                message.user_id, session_id=message.session_id
            )
            self.logging_provider.debug(
                f"Fetched {len(recent_messages)} recent messages"
            )

            history_specs = [
                ChatMessageSpec.model_validate(m.model_dump()) for m in recent_messages
            ]
            history_specs.append(message)

            reply = await self.chatbot_provider.handle_multi_turn(history_specs)

            self.logging_provider.debug("LLM reply generated for contextual chat")

            session_id = await self.__update_chat_session(
                reply, message.user_id, message.session_id
            )

            user_message = message.model_copy(update={"session_id": session_id})
            await self.chatbot_history_accessor.save_message(user_message)
            self.logging_provider.debug("User message saved to chat history")

            reply_timestamp = DateTimeUtils.get_utc_now()
            assistant_message = self.__create_chat_message_spec(
                user_id=message.user_id,
                role=ChatbotMessageRole.ASSISTANT,
                content=reply,
                timestamp=reply_timestamp,
                session_id=session_id,
            )
            await self.chatbot_history_accessor.save_message(assistant_message)
            self.logging_provider.debug("Assistant message saved to chat history")

            return reply
        except Exception as e:
            self.logging_provider.error(f"Error in chat_with_context: {str(e)}")
            raise

    async def get_recipe_title_suggestions(self, user_id: int) -> list[str]:
        """Return four quick recipe title ideas as a simple list of strings."""

        prompt = (
            "Suggest four distinct recipe titles. "
            "Respond only with a JSON array of four strings."
        )
        message = self.__create_chat_message_spec(
            user_id=user_id,
            role=ChatbotMessageRole.USER,
            content=prompt,
            timestamp=DateTimeUtils.get_utc_now(),
        )
        reply = await self.chatbot_provider.handle_single_turn(message)
        try:
            data = json.loads(reply)
            if not isinstance(data, list):
                raise ValueError("Response not list")
            return [str(t) for t in data]
        except Exception:
            self.logging_provider.error(
                "Failed to parse recipe title suggestions", extra_data={"reply": reply}
            )
            raise ValueError("Invalid response from chatbot provider")

    def __create_chat_message_spec(
        self,
        user_id: int,
        role: ChatbotMessageRole,
        content: str,
        timestamp: datetime,
        session_id: Optional[int] = None,
    ) -> ChatMessageSpec:
        """
        Helper to constructs a ChatMessageSpec from components.

        :param user_id: User's ID
        :param role: Sender's role
        :param content: Message text
        :param timestamp: Timestamp of message creation
        :param session_id: Chat session id
        :return: ChatMessageSpec
        """
        return ChatMessageSpec(
            user_id=user_id,
            role=role,
            content=content,
            timestamp=timestamp,
            session_id=session_id,
        )

    def __prepend_format_instruction(
        self, messages: List[ChatMessageSpec]
    ) -> List[ChatMessageSpec]:
        system_msg = ChatMessageSpec(
            user_id=messages[0].user_id,
            role=ChatbotMessageRole.SYSTEM,
            content=self._json_instruction,
            timestamp=DateTimeUtils.get_utc_now(),
            session_id=messages[0].session_id,
        )
        return [system_msg, *messages]

    async def __update_chat_session(
        self, reply: str, user_id: int, session_id: Optional[int]
    ) -> Optional[int]:
        session_data = self.__parse_recipe_reply(reply, user_id)
        if session_data is None:
            return session_id
        await self.chat_session_service.update_session_recipe(session_id, session_data)
        return session_id

    def __parse_recipe_reply(
        self, reply: str, user_id: int
    ) -> Optional[ChatSessionDomain]:
        """Return a ChatSessionDomain if reply contains recipe JSON."""
        try:
            data = json.loads(reply)
        except Exception:
            return None

        if not isinstance(data, dict) or "title" not in data:
            return None

        prep = data.get("prep_time")
        if isinstance(prep, str):
            hours_match = re.search(r"(\d+)\s*(?:h|hr|hrs|hour|hours)", prep, re.I)
            mins_match = re.search(r"(\d+)\s*(?:m|min|mins|minute|minutes)", prep, re.I)
            total = 0
            if hours_match:
                total += int(hours_match.group(1)) * 60
            if mins_match:
                total += int(mins_match.group(1))
            if not hours_match and not mins_match:
                digits = "".join(ch for ch in prep if ch.isdigit())
                total = int(digits) if digits else 0
            prep = total or None

        available = data.get("available_ingredients", 0)
        if isinstance(available, list):
            available = len(available)

        return ChatSessionDomain.create(
            user_id=user_id,
            title=data.get("title", ""),
            summary=data.get("summary"),
            prep_time=prep,
            instructions=data.get("instructions", []),
            ingredients=data.get("ingredients", []),
            available_ingredients=available,
            total_ingredients=data.get(
                "total_ingredients", len(data.get("ingredients", []))
            ),
        )
