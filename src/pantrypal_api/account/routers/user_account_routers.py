from fastapi import APIRouter, Depends, HTTPException, status

from src.core.account.services.auth_service import AuthService
from src.core.account.services.user_account_service import UserAccountService
from src.pantrypal_api.account.controllers.user_account_controller import (
    UserAccountController,
)
from src.pantrypal_api.account.dependencies import get_current_user, oauth2_scheme
from src.pantrypal_api.account.schemas.user_account_schemas import (
    AuthTokenOut,
    LoginUserIn,
    RegisterUserIn,
    UpdateUserIn,
    UserOut,
)
from src.pantrypal_api.modules import injector

router = APIRouter(prefix="/account", tags=["Account"])


# Dependency factory function for controller with injected services
def get_account_controller() -> UserAccountController:
    auth_service = injector.get(AuthService)
    user_service = injector.get(UserAccountService)
    return UserAccountController(auth_service=auth_service, user_service=user_service)


@router.post("/register", response_model=UserOut)
async def register_user(
    data: RegisterUserIn,
    controller: UserAccountController = Depends(get_account_controller),
):
    try:
        return await controller.register_user(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AuthTokenOut)
async def login_user(
    data: LoginUserIn,
    controller: UserAccountController = Depends(get_account_controller),
):
    try:
        return await controller.login(data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout")
async def logout_user(
    token: str = Depends(oauth2_scheme),
    current_user_id: int = Depends(get_current_user),
    controller: UserAccountController = Depends(get_account_controller),
):
    await controller.logout(token)
    return {"detail": "Logged out successfully"}


@router.put("/update", response_model=UserOut)
async def update_user(
    data: UpdateUserIn,
    current_user_id: int = Depends(get_current_user),
    controller: UserAccountController = Depends(get_account_controller),
):
    return await controller.update_user(current_user_id, data)


@router.delete("/delete")
async def delete_user(
    current_user_id: int = Depends(get_current_user),
    controller: UserAccountController = Depends(get_account_controller),
):
    await controller.delete_user(current_user_id)
    return {"detail": "User deleted successfully"}
