from typing import Dict, List

from groq import Groq
from injector import inject

from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider


class GroqChatbotProvider(IChatbotProvider):
    @inject
    def __init__(self, secret_provider: ISecretProvider):
        self.secret_provider = secret_provider

    async def generate_first_reply(self, user_message):
        api_key = self.__get_api_key()
        model = self.__get_model()
        client = Groq(api_key=api_key)

        formatted_messages = self.__format_messages(user_message)

        response = client.chat.completions.create(
            model=model, messages=formatted_messages, max_tokens=1024
        )
        return response.choices[0].message.content

    async def generate_reply(self, messages: List[Dict[str, str]]) -> str:
        api_key = self.__get_api_key()
        model = self.__get_model()
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model=model, messages=messages, max_tokens=1024
        )
        return response.choices[0].message.content

    def __get_api_key(self):
        return self.secret_provider.get_secret(SecretKey.GROQ_API_KEY)

    def __get_model(self):
        return self.secret_provider.get_secret(SecretKey.CHATBOT_MODEL)

    def __format_messages(self, message: str) -> List[Dict[str, str]]:
        return [{"role": "user", "content": message}]
