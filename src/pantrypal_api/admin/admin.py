from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from sqladmin import Admin

from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.admin.account.account_admin import (
    AuthTokenAdmin,
    UserAccountAdmin,
)
from src.pantrypal_api.admin.chatbot.chat_history_admin import ChatHistoryAdmin
from src.pantrypal_api.admin.chatbot.chat_session_admin import ChatSessionAdmin
from src.pantrypal_api.admin.configuration.configuration_admin import ConfigurationAdmin
from src.pantrypal_api.admin.pantry.pantry_item_admin import PantryItemAdmin


def setup_admin(app: FastAPI, db_provider: IDatabaseProvider):
    """
    Initializes the SQLAdmin interface with custom homepage and registers model views.

    :param app: FastAPI instance
    :param db_provider: Database provider containing the SQLAlchemy engine
    """

    # Directly access the engine from provider
    engine = db_provider.engine
    # Use CustomAdmin instead of Admin
    admin = PantryPalAdminSite(app, engine)

    # Register admin views
    admin.add_view(UserAccountAdmin)
    admin.add_view(AuthTokenAdmin)
    admin.add_view(ChatHistoryAdmin)
    admin.add_view(ChatSessionAdmin)
    admin.add_view(ConfigurationAdmin)
    admin.add_view(PantryItemAdmin)


class PantryPalAdminSite(Admin):
    async def index(self, request: Request) -> HTMLResponse:
        view_cards = "\n".join(
            f"""
            <div class="col-12 col-md-6 col-lg-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h3 class="card-title">{view.name_plural}</h3>
                        <p class="text-muted">Manage and inspect <strong>{view.name_plural.lower()}</strong> data.</p>
                        <a href="/admin/{view.identity}/list" class="btn btn-primary w-100">Open</a>
                    </div>
                </div>
            </div>
            """
            for view in self._views
        )

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>PantryPal Admin</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link href="https://unpkg.com/@tabler/core@latest/dist/css/tabler.min.css" rel="stylesheet"/>
            <style>
                body {{
                    background-color: #f8fafc;
                    font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    margin: 0;
                }}
                .admin-header {{
                    background-color: #fff;
                    padding: 2.5rem 1.5rem 2rem;
                    text-align: center;
                    border-bottom: 1px solid #e0e0e0;
                }}
                .admin-header h1 {{
                    font-size: 2.25rem;
                    font-weight: 700;
                    margin: 0;
                }}
                .admin-header p {{
                    font-size: 1rem;
                    color: #6c757d;
                    margin-top: 0.5rem;
                }}
                .card-title {{
                    font-size: 1.125rem;
                    font-weight: 600;
                }}
                .container-xl {{
                    max-width: 1140px;
                }}
            </style>
        </head>
        <body>
            <div class="page">
                <header class="admin-header">
                    <h1>🔍 PantryPal Admin Dashboard</h1>
                    <p>Administer your system data with ease — browse, edit, and monitor core resources below.</p>
                </header>
                <div class="container-xl mt-4">
                    <div class="row g-4">
                        {view_cards}
                    </div>
                    <p class="text-center text-muted mt-4"><em>{len(self._views)} models registered.</em></p>
                </div>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=html)
