from typing import Optional

from injector import inject
from sqlalchemy import select

from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.receipt.accessors.receipt_result_accessor import IReceiptResultAccessor
from src.core.receipt.models import ReceiptResultDomain
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.receipt.models import ReceiptResult


class ReceiptResultAccessor(IReceiptResultAccessor):
    @inject
    def __init__(
        self, db_provider: IDatabaseProvider, logging_provider: ILoggingProvider
    ) -> None:
        self.db_provider = db_provider
        self.logging_provider = logging_provider

    async def get_result(
        self, user_id: int, receipt_id: str
    ) -> Optional[ReceiptResultDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(ReceiptResult).where(
                    ReceiptResult.user_id == user_id,
                    ReceiptResult.receipt_id == receipt_id,
                )
            )
            record = result.scalar_one_or_none()
            return record.to_domain() if record else None

    async def add_result(self, result: ReceiptResultDomain) -> ReceiptResultDomain:
        async with self.db_provider.get_db() as db:
            record = ReceiptResult(
                user_id=result.user_id,
                receipt_id=result.receipt_id,
                result=result.result,
            )
            db.add(record)
            await db.commit()
            return record.to_domain()
