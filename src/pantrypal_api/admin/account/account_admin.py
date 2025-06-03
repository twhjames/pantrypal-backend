from src.pantrypal_api.account.models import AuthToken, UserAccount
from src.pantrypal_api.admin.base.admin import PantryPalModelAdmin


class UserAccountAdmin(PantryPalModelAdmin, model=UserAccount):
    name = "User Account"
    name_plural = "User Accounts"
    icon = "fa-solid fa-user"

    column_list = [
        UserAccount.id,
        UserAccount.username,
        UserAccount.email,
        UserAccount.password_hash,
        UserAccount.created_at,
        UserAccount.updated_at,
    ]

    form_columns = [
        UserAccount.username,
        UserAccount.email,
        UserAccount.password_hash,
    ]

    column_searchable_list = [
        UserAccount.username,
        UserAccount.email,
    ]


class AuthTokenAdmin(PantryPalModelAdmin, model=AuthToken):
    name = "Auth Token"
    name_plural = "Auth Tokens"
    icon = "fa-solid fa-key"

    column_list = [
        AuthToken.id,
        AuthToken.user_id,
        AuthToken.token,
        AuthToken.token_issued_at,
        AuthToken.expires_at,
        AuthToken.created_at,
        AuthToken.updated_at,
    ]

    column_searchable_list = [
        AuthToken.token,
    ]
