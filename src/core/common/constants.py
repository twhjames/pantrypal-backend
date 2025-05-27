from enum import Enum


class SecretKey(str, Enum):
    GROQ_API_KEY = "GROQ_API_KEY"
    CHATBOT_MODEL = "CHATBOT_MODEL"
