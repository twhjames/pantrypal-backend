from injector import Injector

from src.pantrypal_api.chatbot.modules import ChatbotModule
from src.pantrypal_api.common.modules import CommonModule
from src.pantrypal_api.configuration.modules import ConfigurationModule
from src.pantrypal_api.storage.modules import StorageModule

injector = Injector([ChatbotModule, CommonModule, ConfigurationModule, StorageModule])
