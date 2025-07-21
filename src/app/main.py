from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

from src.app.middleware import setup_middlewares
from src.app.router_setup import setup_routers
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.admin.admin import setup_admin
from src.pantrypal_api.modules import injector

# Inject logger
logger = injector.get(ILoggingProvider)


def create_app() -> FastAPI:
    # Log application initialization
    logger.info("Initializing PantryPal API server...", tag="Startup")

    # Lifespan event handler to ensure default admin user exists on app startup
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        secret_provider = injector.get(ISecretProvider)
        username = secret_provider.get_secret(SecretKey.ADMIN_USERNAME)
        email = secret_provider.get_secret(SecretKey.ADMIN_EMAIL)
        password = secret_provider.get_secret(SecretKey.ADMIN_PASSWORD)
        if not all([username, email, password]):
            logger.warning(
                "Admin credentials are not fully configured; admin login will be disabled",
                tag="Startup",
            )
        yield

    # Initialize the FastAPI app
    app = FastAPI(
        title="PantryPal API",
        description="Smart pantry assistant backend with inventory, recipe, and chatbot support",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Apply middlewares (CORS)
    setup_middlewares(app)

    # Health check route
    @app.get("/", tags=["Health"])
    def root():
        return {"message": "PantryPal API is running"}

    # Protected Swagger UI docs, accessible only to authenticated admin users
    @app.get("/docs", include_in_schema=False)
    async def custom_docs():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=f"{app.title} Docs",
        )

    # Register routers
    setup_routers(app)

    # Register admin views using injected database provider
    db_provider = injector.get(IDatabaseProvider)
    setup_admin(app, db_provider)

    # Log successful application setup
    logger.info("PantryPal API setup completed", tag="Startup")

    return app


app = create_app()
