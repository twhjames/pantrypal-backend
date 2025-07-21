from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.modules import injector


class AdminRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path == "/docs" or (
            path.startswith("/admin") and not path.startswith("/admin/login")
        ):
            token = request.headers.get("Authorization") or request.cookies.get(
                "Authorization"
            )
            if token:
                scheme, param = get_authorization_scheme_param(str(token))
                if scheme.lower() != "bearer":
                    param = str(token)
                if param:
                    auth_service = injector.get(AuthService)
                    user_service = injector.get(UserAccountService)
                    try:
                        user_id = await auth_service.verify_auth_token(param)
                        user = await user_service.get_user(user_id)
                        if user and user.is_admin:
                            return await call_next(request)
                    except Exception:
                        pass
            return RedirectResponse(url="/admin/login")

        return await call_next(request)


def setup_middlewares(app: FastAPI):
    # allow_origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AdminRedirectMiddleware)
