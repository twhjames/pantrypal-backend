from injector import Injector

from src.pantrypal_api.chatbot.modules import ChatbotModule
from src.pantrypal_api.common.modules import CommonModule

injector = Injector([ChatbotModule, CommonModule])
