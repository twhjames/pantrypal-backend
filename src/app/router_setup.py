from fastapi import FastAPI

from src.pantrypal_api.account.routers.user_account_routers import (
    router as account_routers,
)
from src.pantrypal_api.admin.routes import router as admin_routers
from src.pantrypal_api.chatbot.routers.chatbot_routers import router as chatbot_routers
from src.pantrypal_api.pantry.routers.pantry_routers import router as pantry_routers
from src.pantrypal_api.receipt.routers.receipt_router import router as receipt_router

# Add other routers here as app grows


def setup_routers(app: FastAPI):
    app.include_router(admin_routers)
    app.include_router(account_routers)
    app.include_router(chatbot_routers)
    app.include_router(pantry_routers)
    app.include_router(receipt_router)
