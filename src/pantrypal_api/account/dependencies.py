from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from src.core.account.models import UserAccountDomain
from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.modules import injector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login", auto_error=False)


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> int:
    if not token:
        cookie_auth = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(cookie_auth or "")
        if scheme.lower() == "bearer" and param:
            token = param
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

    auth_service = injector.get(AuthService)
    user_service = injector.get(UserAccountService)
    user_id = await auth_service.verify_auth_token(token)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user.id


async def get_current_user_obj(
    request: Request,
    token: str = Depends(oauth2_scheme),
) -> "UserAccountDomain":
    if not token:
        cookie_auth = request.cookies.get("Authorization")
        scheme, param = get_authorization_scheme_param(cookie_auth or "")
        if scheme.lower() == "bearer" and param:
            token = param
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

    auth_service = injector.get(AuthService)
    user_service = injector.get(UserAccountService)
    user_id = await auth_service.verify_auth_token(token)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


async def admin_required(user=Depends(get_current_user_obj)) -> int:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Administrator access required",
        )
    return user.id
