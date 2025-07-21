from datetime import datetime, timedelta, timezone
from typing import List

from injector import inject

from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.pantry.accessors.pantry_item_accessor import IPantryItemAccessor
from src.core.pantry.models import PantryItemDomain, PantryStatsDomain
from src.core.pantry.specs import (
    AddPantryItemSpec,
    DeletePantryItemsSpec,
    UpdatePantryItemSpec,
)


class PantryService:
    @inject
    def __init__(
        self,
        pantry_accessor: IPantryItemAccessor,
        logging_provider: ILoggingProvider,
    ):
        self.pantry_accessor = pantry_accessor
        self.logging_provider = logging_provider

    async def get_items(self, user_id: int) -> List[PantryItemDomain]:
        return await self.pantry_accessor.get_items_by_user(user_id)

    async def add_items(
        self, user_id: int, specs: List[AddPantryItemSpec]
    ) -> List[PantryItemDomain]:
        domains = [
            PantryItemDomain.create(
                user_id=user_id,
                item_name=spec.item_name,
                quantity=spec.quantity,
                unit=spec.unit,
                category=spec.category,
                purchase_date=spec.purchase_date,
                expiry_date=spec.expiry_date,
            )
            for spec in specs
        ]
        return await self.pantry_accessor.add_items(domains)

    async def update_item(
        self, user_id: int, spec: UpdatePantryItemSpec
    ) -> PantryItemDomain:
        existing = await self.pantry_accessor.get_item_by_id(spec.id, user_id)
        if not existing:
            self.logging_provider.warning(
                "Attempted update of non-existent pantry item",
                extra_data={"user_id": user_id, "item_id": spec.id},
                tag="PantryService",
            )
            raise ValueError("Pantry item not found")

        updated = PantryItemDomain(
            id=existing.id,
            user_id=existing.user_id,
            item_name=spec.item_name or existing.item_name,
            quantity=spec.quantity if spec.quantity is not None else existing.quantity,
            unit=spec.unit or existing.unit,
            category=spec.category if spec.category is not None else existing.category,
            purchase_date=spec.purchase_date
            if spec.purchase_date is not None
            else existing.purchase_date,
            expiry_date=spec.expiry_date
            if spec.expiry_date is not None
            else existing.expiry_date,
            created_at=existing.created_at,
            updated_at=DateTimeUtils.get_utc_now(),
        )
        return await self.pantry_accessor.update_item(updated)

    async def delete_items(self, user_id: int, spec: DeletePantryItemsSpec) -> None:
        # validate if items exist and belong to user
        existing_items = await self.pantry_accessor.get_items_by_ids(
            spec.item_ids, user_id
        )

        if len(existing_items) != len(spec.item_ids):
            missing_ids = set(spec.item_ids) - {item.id for item in existing_items}
            self.logging_provider.warning(
                "Attempted to delete non-existent or unauthorized items",
                extra_data={"user_id": user_id, "missing_item_ids": list(missing_ids)},
                tag="PantryService",
            )
            raise ValueError(
                f"Some items do not exist or do not belong to the user: {missing_ids}"
            )

        return await self.pantry_accessor.delete_items(
            item_ids=spec.item_ids,
            user_id=user_id,
        )

    async def get_items_sorted_by_expiry(self, user_id: int) -> List[PantryItemDomain]:
        items = await self.get_items(user_id)
        max_dt = datetime.max.replace(tzinfo=timezone.utc)

        def _key(item: PantryItemDomain) -> datetime:
            if item.expiry_date is None:
                return max_dt
            return (
                item.expiry_date
                if item.expiry_date.tzinfo
                else item.expiry_date.replace(tzinfo=timezone.utc)
            )

        return sorted(items, key=_key)

    async def get_pantry_stats(self, user_id: int) -> PantryStatsDomain:
        items = await self.get_items(user_id)
        now = DateTimeUtils.get_utc_now()
        today = now.date()
        soon_threshold = today + timedelta(days=7)

        total = len(items)
        expired = 0
        expiring_today = 0
        expiring_soon = 0

        for item in items:
            if not item.expiry_date:
                continue
            expiry_date = item.expiry_date.date()
            if expiry_date < today:
                expired += 1
            elif expiry_date == today:
                expiring_today += 1
            elif today < expiry_date <= soon_threshold:
                expiring_soon += 1

        return PantryStatsDomain(
            total_items=total,
            expiring_soon=expiring_soon,
            expiring_today=expiring_today,
            expired=expired,
        )

    async def get_expiring_items(self, user_id: int) -> List[PantryItemDomain]:
        items = await self.get_items(user_id)
        now = DateTimeUtils.get_utc_now()
        threshold = now + timedelta(days=7)
        expiring: List[PantryItemDomain] = []
        for item in items:
            if not item.expiry_date:
                continue
            expiry = (
                item.expiry_date
                if item.expiry_date.tzinfo
                else item.expiry_date.replace(tzinfo=timezone.utc)
            )
            if expiry <= threshold:
                # store timezone-aware copy to avoid comparison issues later
                item.expiry_date = expiry
                expiring.append(item)
        max_dt = datetime.max.replace(tzinfo=timezone.utc)

        def _key(item: PantryItemDomain) -> datetime:
            return item.expiry_date or max_dt

        return sorted(expiring, key=_key)[:3]
