from datetime import datetime, timedelta, timezone

import pytest

from src.core.common.utils import DateTimeUtils
from src.core.pantry.constants import Category, Unit
from src.core.pantry.models import PantryItemDomain
from src.core.pantry.services.pantry_service import PantryService
from src.core.pantry.specs import (
    AddPantryItemSpec,
    DeletePantryItemsSpec,
    UpdatePantryItemSpec,
)


@pytest.mark.asyncio
async def test_get_items_returns_user_items(
    mock_pantry_item_accessor, mock_logging_provider
):
    now = datetime.now(timezone.utc)
    mock_pantry_item_accessor.get_items_by_user.return_value = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="Milk",
            quantity=1.0,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=None,
            created_at=now,
            updated_at=now,
        )
    ]

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    items = await service.get_items(user_id=1)

    assert len(items) == 1
    assert items[0].item_name == "Milk"


@pytest.mark.asyncio
async def test_add_items_creates_items(
    mock_pantry_item_accessor, mock_logging_provider
):
    spec = AddPantryItemSpec(
        item_name="Apple",
        quantity=2.0,
        unit=Unit.GRAMS,
        category=Category.FRUITS,
        purchase_date=None,
        expiry_date=None,
    )

    now = datetime.now(timezone.utc)
    pantry_item = PantryItemDomain(
        id=1,
        user_id=1,
        item_name="Apple",
        quantity=2.0,
        unit=Unit.GRAMS,
        category=Category.FRUITS,
        purchase_date=None,
        expiry_date=None,
        created_at=now,
        updated_at=now,
    )

    mock_pantry_item_accessor.add_items.return_value = [pantry_item]

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.add_items(user_id=1, specs=[spec])

    assert len(result) == 1
    assert result[0].item_name == "Apple"


@pytest.mark.asyncio
async def test_update_item_success(mock_pantry_item_accessor, mock_logging_provider):
    now = datetime.now(timezone.utc)
    existing_item = PantryItemDomain(
        id=1,
        user_id=1,
        item_name="Old",
        quantity=1.0,
        unit=Unit.GRAMS,
        category=Category.FRUITS,
        purchase_date=now,
        expiry_date=now,
        created_at=now,
        updated_at=now,
    )

    updated_item = existing_item.model_copy(
        update={"item_name": "New", "quantity": 2.0, "updated_at": now}
    )

    mock_pantry_item_accessor.get_item_by_id.return_value = existing_item
    mock_pantry_item_accessor.update_item.return_value = updated_item

    spec = UpdatePantryItemSpec(
        id=1,
        item_name="New",
        quantity=2.0,
        unit=Unit.GRAMS,
        category=Category.FRUITS,
        purchase_date=now,
        expiry_date=now,
    )

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.update_item(user_id=1, spec=spec)

    assert result.item_name == "New"
    assert result.quantity == 2.0


@pytest.mark.asyncio
async def test_delete_items_success(mock_pantry_item_accessor, mock_logging_provider):
    now = datetime.now(timezone.utc)
    pantry_item = PantryItemDomain(
        id=1,
        user_id=1,
        item_name="Apple",
        quantity=1.0,
        unit=Unit.GRAMS,
        category=Category.FRUITS,
        purchase_date=None,
        expiry_date=None,
        created_at=now,
        updated_at=now,
    )

    mock_pantry_item_accessor.get_items_by_ids.return_value = [pantry_item]

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    spec = DeletePantryItemsSpec(item_ids=[1])

    await service.delete_items(user_id=1, spec=spec)
    mock_pantry_item_accessor.delete_items.assert_awaited_once_with(
        item_ids=[1], user_id=1
    )


@pytest.mark.asyncio
async def test_get_items_sorted_by_expiry(
    mock_pantry_item_accessor, mock_logging_provider
):
    now = datetime.now(timezone.utc)
    items = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="A",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=2),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=2,
            user_id=1,
            item_name="B",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=1),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=3,
            user_id=1,
            item_name="C",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=None,
            created_at=now,
            updated_at=now,
        ),
    ]

    mock_pantry_item_accessor.get_items_by_user.return_value = items

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.get_items_sorted_by_expiry(user_id=1)

    assert [i.id for i in result] == [2, 1, 3]


@pytest.mark.asyncio
async def test_get_pantry_stats(mock_pantry_item_accessor, mock_logging_provider):
    now = DateTimeUtils.get_utc_now()
    items = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="Expired",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now - timedelta(days=1),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=2,
            user_id=1,
            item_name="Today",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now,
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=3,
            user_id=1,
            item_name="Soon",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=3),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=4,
            user_id=1,
            item_name="Later",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=20),
            created_at=now,
            updated_at=now,
        ),
    ]

    mock_pantry_item_accessor.get_items_by_user.return_value = items

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    stats = await service.get_pantry_stats(user_id=1)

    assert stats.total_items == 4
    assert stats.expired == 1
    assert stats.expiring_today == 1
    assert stats.expiring_soon == 1


@pytest.mark.asyncio
async def test_get_expiring_items(mock_pantry_item_accessor, mock_logging_provider):
    now = DateTimeUtils.get_utc_now()
    items = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="Expired",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now - timedelta(days=1),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=2,
            user_id=1,
            item_name="Soon",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=3),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=3,
            user_id=1,
            item_name="Later",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=10),
            created_at=now,
            updated_at=now,
        ),
    ]

    mock_pantry_item_accessor.get_items_by_user.return_value = items

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.get_expiring_items(user_id=1)

    assert [i.id for i in result] == [1, 2]


@pytest.mark.asyncio
async def test_get_expiring_items_handles_naive_datetimes(
    mock_pantry_item_accessor, mock_logging_provider, monkeypatch
):
    """Ensure naive expiry dates do not cause comparison errors."""
    now = DateTimeUtils.get_utc_now()
    monkeypatch.setattr(DateTimeUtils, "get_utc_now", lambda: now)
    items = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="Expired",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=(now - timedelta(days=1)).replace(tzinfo=None),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=2,
            user_id=1,
            item_name="Soon",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=(now + timedelta(days=3)).replace(tzinfo=None),
            created_at=now,
            updated_at=now,
        ),
    ]

    mock_pantry_item_accessor.get_items_by_user.return_value = items

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.get_expiring_items(user_id=1)

    assert [i.id for i in result] == [1, 2]


@pytest.mark.asyncio
async def test_get_expiring_items_returns_top_three(
    mock_pantry_item_accessor, mock_logging_provider, monkeypatch
):
    """Only the three soonest expiring items are returned."""
    now = DateTimeUtils.get_utc_now()
    monkeypatch.setattr(DateTimeUtils, "get_utc_now", lambda: now)
    items = [
        PantryItemDomain(
            id=1,
            user_id=1,
            item_name="Expired",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now - timedelta(days=1),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=2,
            user_id=1,
            item_name="Soon1",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=1),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=3,
            user_id=1,
            item_name="Soon2",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=2),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=4,
            user_id=1,
            item_name="Soon3",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=3),
            created_at=now,
            updated_at=now,
        ),
        PantryItemDomain(
            id=5,
            user_id=1,
            item_name="Soon4",
            quantity=1,
            unit=Unit.GRAMS,
            category=Category.FRUITS,
            purchase_date=None,
            expiry_date=now + timedelta(days=4),
            created_at=now,
            updated_at=now,
        ),
    ]

    mock_pantry_item_accessor.get_items_by_user.return_value = items

    service = PantryService(mock_pantry_item_accessor, mock_logging_provider)
    result = await service.get_expiring_items(user_id=1)

    assert [i.id for i in result] == [1, 2, 3]
