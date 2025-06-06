from injector import inject
from sqlalchemy import delete, select

from src.core.account.accessors.auth_token_accessor import IAuthTokenAccessor
from src.core.account.models import AuthTokenDomain
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.account.models import AuthToken


class AuthTokenAccessor(IAuthTokenAccessor):
    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
    ):
        self.db_provider = db_provider

    async def upsert(self, auth_token: AuthTokenDomain) -> AuthTokenDomain:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(AuthToken).filter_by(user_id=auth_token.user_id)
            )
            record = result.scalar_one_or_none()

            if record:
                for field, value in auth_token.model_dump(
                    exclude={"id", "created_at", "updated_at"}
                ).items():
                    setattr(record, field, value)
            else:
                record = self.__to_model(auth_token)
                db.add(record)

            await db.commit()
            await db.refresh(record)
            return record.to_domain()

    async def get_by_token(self, token: str) -> AuthTokenDomain | None:
        async with self.db_provider.get_db() as db:
            result = await db.execute(select(AuthToken).filter_by(token=token))
            record = result.scalar_one_or_none()
            return record.to_domain() if record else None

    async def delete_by_token(self, token: str) -> None:
        async with self.db_provider.get_db() as db:
            await db.execute(delete(AuthToken).where(AuthToken.token == token))
            await db.commit()

    async def delete_by_user_id(self, user_id: int) -> None:
        async with self.db_provider.get_db() as db:
            await db.execute(delete(AuthToken).where(AuthToken.user_id == user_id))
            await db.commit()

    def __to_model(self, domain: AuthTokenDomain) -> AuthToken:
        return AuthToken(
            token=domain.token,
            user_id=domain.user_id,
            token_issued_at=domain.token_issued_at,
            expires_at=domain.expires_at,
        )
