import asyncio
from typing import Dict, List

from groq import BadRequestError, Groq
from injector import inject

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider


class GroqChatbotProvider(IChatbotProvider):
    """Handles interaction with Groq LLM for both single-turn and multi-turn chat."""

    @inject
    def __init__(self, secret_provider: ISecretProvider):
        self.secret_provider = secret_provider

    async def handle_single_turn(self, message: ChatMessageSpec) -> str:
        """Processes a single-turn message."""
        formatted_messages = [self.__format_message(message)]
        return await self.__call_groq(formatted_messages)

    async def handle_multi_turn(self, messages: List[ChatMessageSpec]) -> str:
        """Processes multi-turn messages with history."""
        formatted_history = [self.__format_message(m) for m in messages]
        return await self.__call_groq(formatted_history)

    async def __call_groq(self, formatted_messages: List[Dict[str, str]]) -> str:
        """Executes the synchronous Groq API call in a separate thread to avoid blocking the event loop."""
        return await asyncio.to_thread(self.__sync_call_groq, formatted_messages)

    def __sync_call_groq(self, formatted_messages: List[Dict[str, str]]) -> str:
        """Executes the chat completion request to Groq."""
        api_key = self.__get_api_key()
        model = self.__get_model()
        max_tokens = self.__get_max_tokens()
        client = Groq(api_key=api_key)

        try:
            response = client.chat.completions.create(
                model=model, messages=formatted_messages, max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except BadRequestError as e:
            raise RuntimeError(f"Groq API call failed: {e}")

    def __format_message(self, message: ChatMessageSpec) -> Dict[str, str]:
        """Formats internal message spec into Groq-compatible format."""
        return {"role": message.role.value.lower(), "content": message.content}

    def __get_api_key(self) -> str:
        return self.secret_provider.get_secret(SecretKey.GROQ_API_KEY)

    def __get_model(self) -> str:
        return self.secret_provider.get_secret(SecretKey.CHATBOT_MODEL)

    def __get_max_tokens(self) -> int:
        try:
            return int(self.secret_provider.get_secret(SecretKey.CHATBOT_MAX_TOKENS))
        except (TypeError, ValueError):
            raise ValueError("Invalid CHATBOT_MAX_TOKENS value in .env")
