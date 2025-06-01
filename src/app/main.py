from fastapi import FastAPI

from src.app.logging import setup_logging
from src.app.middleware import setup_middlewares
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.admin.admin import setup_admin
from src.pantrypal_api.chatbot.routers import chatbot_routers
from src.pantrypal_api.modules import injector


def create_app() -> FastAPI:
    # Setup logging
    setup_logging()

    # Initialize the FastAPI app
    app = FastAPI(
        title="PantryPal API",
        description="Smart pantry assistant backend with inventory, recipe, and chatbot support",
        version="1.0.0",
    )

    # Apply middlewares (CORS)
    setup_middlewares(app)

    # Health check route
    @app.get("/", tags=["Health"])
    def root():
        return {"message": "PantryPal API is running"}

    # Register routers
    app.include_router(chatbot_routers.router)

    # Register admin views using injected database provider
    db_provider = injector.get(IDatabaseProvider)
    setup_admin(app, db_provider)

    return app


app = create_app()
