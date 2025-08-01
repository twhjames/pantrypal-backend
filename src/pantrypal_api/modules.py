from injector import Injector

from src.pantrypal_api.account.modules import AccountModule
from src.pantrypal_api.chatbot.modules import ChatbotModule
from src.pantrypal_api.common.modules import CommonModule
from src.pantrypal_api.configuration.modules import ConfigurationModule
from src.pantrypal_api.expiry.modules import ExpiryModule
from src.pantrypal_api.logging.modules import LoggingModule
from src.pantrypal_api.pantry.modules import PantryModule
from src.pantrypal_api.receipt.modules import ReceiptModule
from src.pantrypal_api.storage.modules import StorageModule

injector = Injector(
    [
        AccountModule,
        ChatbotModule,
        CommonModule,
        ConfigurationModule,
        ExpiryModule,
        PantryModule,
        ReceiptModule,
        StorageModule,
        LoggingModule,
    ]
)
