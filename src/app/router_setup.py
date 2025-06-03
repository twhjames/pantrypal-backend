from fastapi import FastAPI

from src.pantrypal_api.account.routers.user_account_routers import (
    router as account_routers,
)
from src.pantrypal_api.chatbot.routers.chatbot_routers import router as chatbot_routers

# Add other routers here as app grows


def setup_routers(app: FastAPI):
    app.include_router(chatbot_routers)
    app.include_router(account_routers)
