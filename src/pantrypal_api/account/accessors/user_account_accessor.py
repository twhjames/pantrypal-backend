from typing import Optional

from injector import inject
from sqlalchemy import delete, select

from src.core.account.accessors.user_account_accessor import IUserAccountAccessor
from src.core.account.models import UserAccountDomain
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.account.models import UserAccount


class UserAccountAccessor(IUserAccountAccessor):
    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
        logging_provider: ILoggingProvider,
    ):
        self.db_provider = db_provider
        self.logging_provider = logging_provider

    async def get_by_id(self, user_id: int) -> Optional[UserAccountDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(select(UserAccount).filter_by(id=user_id))
            record = result.scalar_one_or_none()
            return record.to_domain() if record else None

    async def get_by_email(self, email: str) -> Optional[UserAccountDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(select(UserAccount).filter_by(email=email))
            record = result.scalar_one_or_none()
            return record.to_domain() if record else None

    async def create_user(self, user: UserAccountDomain) -> UserAccountDomain:
        async with self.db_provider.get_db() as db:
            model = self.__to_model(user)
            db.add(model)
            await db.commit()
            await db.refresh(model)
            return model.to_domain()

    async def update_user(self, user: UserAccountDomain) -> UserAccountDomain:
        async with self.db_provider.get_db() as db:
            result = await db.execute(select(UserAccount).filter_by(id=user.id))
            model = result.scalar_one_or_none()
            if not model:
                self.logging_provider.error(
                    "User not found during update",
                    extra_data={"user_id": user.id},
                    tag="UserAccountAccessor",
                )
                raise ValueError("User not found")
            for field, value in user.model_dump(
                exclude={"id", "created_at", "updated_at"}
            ).items():
                setattr(model, field, value)
            await db.commit()
            await db.refresh(model)
            return model.to_domain()

    async def delete_by_id(self, user_id: int) -> None:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                delete(UserAccount).where(UserAccount.id == user_id)
            )
            if result.rowcount == 0:
                self.logging_provider.warning(
                    "Attempted to delete non-existent user",
                    extra_data={"user_id": user_id},
                    tag="UserAccountAccessor",
                )
            await db.commit()

    def __to_model(self, domain: UserAccountDomain) -> UserAccount:
        return UserAccount(
            username=domain.username,
            email=domain.email,
            password_hash=domain.password_hash,
        )
