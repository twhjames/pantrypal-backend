from fastapi import HTTPException, Request, status
from fastapi.security.utils import get_authorization_scheme_param
from sqladmin.authentication import AuthenticationBackend

from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.core.account.specs import LoginSpec
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.pantrypal_api.modules import injector


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_provider: ISecretProvider | None = None):
        if secret_provider is None:
            secret_provider = injector.get(ISecretProvider)
        self.secret_provider = secret_provider
        secret_key = secret_provider.get_secret(SecretKey.AUTH_SECRET_KEY)
        if not secret_key:
            raise RuntimeError("AUTH_SECRET_KEY is not configured")
        super().__init__(secret_key=secret_key)
        self.secret_key = secret_key

    async def authenticate(self, request: Request) -> bool:
        auth = request.headers.get("Authorization") or request.cookies.get(
            "Authorization"
        )
        if not auth:
            return False
        scheme, token = get_authorization_scheme_param(auth)
        if scheme.lower() != "bearer" or not token:
            return False
        auth_service = injector.get(AuthService)
        user_service = injector.get(UserAccountService)
        user_id = await auth_service.verify_auth_token(token)
        user = await user_service.get_user(user_id)
        if not user or not user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Administrator access required",
            )
        return True

    async def login(self, request: Request) -> bool:
        """Handle admin login for SQLAdmin."""
        form = await request.form()
        email = form.get("email") or form.get("username")
        password = form.get("password")
        if not email or not password:
            return False
        auth_service = injector.get(AuthService)
        user_service = injector.get(UserAccountService)
        try:
            token_domain = await auth_service.login(
                LoginSpec(email=email, password=password)
            )
        except Exception:
            return False
        user = await user_service.get_user(token_domain.user_id)
        if not user or not user.is_admin:
            return False
        # login is handled via a custom route that sets a cookie
        return True

    async def logout(self, request: Request) -> None:
        # logout handled in custom route
        pass
