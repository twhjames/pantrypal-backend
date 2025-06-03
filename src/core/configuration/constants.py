from enum import Enum


class ConfigurationKey(str, Enum):
    NOTIFICATION_EMAIL_SENDER_NAME = "NOTIFICATION_EMAIL_SENDER_NAME"
    NOTIFICATION_EMAIL_SENDER = "NOTIFICATION_EMAIL_SENDER"


class ConfigurationDefault(str, Enum):
    NOTIFICATION_EMAIL_SENDER_NAME = "PantryPal Assistant"
    NOTIFICATION_EMAIL_SENDER = "notification@pantrypal.ai"
