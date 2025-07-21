import asyncio
import sys
from pathlib import Path

from src.core.account.accessors.user_account_accessor import IUserAccountAccessor
from src.core.account.models import UserAccountDomain
from src.core.account.ports.auth_provider import IAuthProvider
from src.core.common.constants import SecretKey
from src.core.common.ports.secretkey_provider import ISecretProvider
from src.pantrypal_api.modules import injector

# Ensure the repository root is on the path so `src` imports work when running
# this script directly via `python scripts/create_superuser.py`.
sys.path.append(str(Path(__file__).resolve().parents[1]))


async def create_superuser() -> None:
    secret_provider = injector.get(ISecretProvider)
    username = secret_provider.get_secret(SecretKey.ADMIN_USERNAME)
    email = secret_provider.get_secret(SecretKey.ADMIN_EMAIL)
    password = secret_provider.get_secret(SecretKey.ADMIN_PASSWORD)
    if not all([username, email, password]):
        print(
            "Missing admin credentials. Set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD in the environment."
        )
        return

    user_accessor: IUserAccountAccessor = injector.get(IUserAccountAccessor)
    auth_provider: IAuthProvider = injector.get(IAuthProvider)

    existing = await user_accessor.get_by_email(email)
    if existing:
        if existing.is_admin:
            print("Admin user already exists.")
            return
        existing.is_admin = True
        await user_accessor.update_user(existing)
        print("Existing user promoted to admin.")
        return

    password_hash = auth_provider.get_hashed_password(password)
    admin = UserAccountDomain.create(
        username=username,
        email=email,
        password_hash=password_hash,
        is_admin=True,
    )
    await user_accessor.create_user(admin)
    print("Admin user created successfully.")


if __name__ == "__main__":
    asyncio.run(create_superuser())
