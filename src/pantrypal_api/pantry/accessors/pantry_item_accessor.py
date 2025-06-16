from typing import List, Optional

from injector import inject
from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound

from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.pantry.accessors.pantry_item_accessor import IPantryItemAccessor
from src.core.pantry.models import PantryItemDomain
from src.core.storage.ports.relational_database_provider import IDatabaseProvider
from src.pantrypal_api.pantry.models import PantryItem


class PantryItemAccessor(IPantryItemAccessor):
    @inject
    def __init__(
        self,
        db_provider: IDatabaseProvider,
        logging_provider: ILoggingProvider,
    ):
        self.db_provider = db_provider
        self.logging_provider = logging_provider

    async def add_items(self, items: List[PantryItemDomain]) -> List[PantryItemDomain]:
        records = [self.__to_model(item) for item in items]

        async with self.db_provider.get_db() as db:
            db.add_all(records)
            await db.commit()
            return [record.to_domain() for record in records]

    async def delete_items(self, item_ids: List[int], user_id: int) -> None:
        async with self.db_provider.get_db() as db:
            stmt = delete(PantryItem).where(
                PantryItem.id.in_(item_ids), PantryItem.user_id == user_id
            )
            result = await db.execute(stmt)
            await db.commit()

            if result.rowcount == 0:
                self.logging_provider.warning(
                    "No pantry items deleted",
                    extra_data={"user_id": user_id, "item_ids": item_ids},
                    tag="PantryItemAccessor",
                )

    async def update_item(self, item: PantryItemDomain) -> PantryItemDomain:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(PantryItem).where(
                    PantryItem.id == item.id, PantryItem.user_id == item.user_id
                )
            )
            record = result.scalar_one_or_none()
            if not record:
                self.logging_provider.warning(
                    "Attempted to update non-existent pantry item",
                    extra_data={"user_id": item.user_id, "item_id": item.id},
                    tag="PantryItemAccessor",
                )
                raise NoResultFound("Pantry item not found for update")

            # Update mutable fields
            record.item_name = item.item_name
            record.quantity = item.quantity
            record.unit = item.unit
            record.category = item.category
            record.expiry_date = item.expiry_date
            record.purchase_date = item.purchase_date

            domain = record.to_domain()  # Force load all fields while session is active
            await db.commit()
            return domain

    async def get_items_by_user(self, user_id: int) -> List[PantryItemDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(PantryItem).where(PantryItem.user_id == user_id)
            )
            records = result.scalars().all()
            return [record.to_domain() for record in records]

    async def get_item_by_id(
        self, item_id: int, user_id: int
    ) -> Optional[PantryItemDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(PantryItem).where(
                    PantryItem.id == item_id, PantryItem.user_id == user_id
                )
            )
            record = result.scalar_one_or_none()
            return record.to_domain() if record else None

    async def get_items_by_ids(
        self, item_ids: List[int], user_id: int
    ) -> List[PantryItemDomain]:
        async with self.db_provider.get_db() as db:
            result = await db.execute(
                select(PantryItem).where(
                    PantryItem.id.in_(item_ids), PantryItem.user_id == user_id
                )
            )
            records = result.scalars().all()
            return [record.to_domain() for record in records]

    @staticmethod
    def __to_model(domain: PantryItemDomain) -> PantryItem:
        return PantryItem(
            user_id=domain.user_id,
            item_name=domain.item_name,
            quantity=domain.quantity,
            unit=domain.unit,
            category=domain.category,
            purchase_date=domain.purchase_date,
            expiry_date=domain.expiry_date,
        )
