from injector import inject

from src.core.chatbot.accessors.chatbot_history_accessor import IChatbotHistoryAccessor
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.services.chatbot_service import ChatbotService
from src.core.chatbot.specs import ChatMessageSpec
from src.pantrypal_api.chatbot.schemas.chatbot_schemas import Message


class ChatbotController:
    @inject
    def __init__(
        self,
        chatbot_provider: IChatbotProvider,
        chat_history_accessor: IChatbotHistoryAccessor,
    ):
        self.chatbot_service = ChatbotService(chatbot_provider, chat_history_accessor)

    async def get_recipe_recommendation(self, message: Message) -> str:
        spec = self.__schema_to_spec(message)
        return await self.chatbot_service.get_first_recommendation(spec)

    async def get_contextual_chat_reply(self, message: Message) -> str:
        specs = self.__schema_to_spec(message)
        return await self.chatbot_service.chat_with_context(specs)

    def __schema_to_spec(
        self,
        message: Message,
    ) -> ChatMessageSpec:
        # Ensures the @model_validator is triggered
        message = message.model_copy()

        return ChatMessageSpec(
            user_id=message.user_id,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp,
        )
