from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.modules import injector

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/account/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> int:
    auth_service = injector.get(AuthService)
    user_service = injector.get(UserAccountService)
    user_id = await auth_service.verify_auth_token(token)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user.id
