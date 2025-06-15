from datetime import datetime, timezone

import pytest

from src.core.pantry.constants import Category, Unit
from src.core.pantry.models import PantryItemDomain
from src.pantrypal_api.pantry.accessors.pantry_item_accessor import PantryItemAccessor


@pytest.mark.asyncio
async def test_add_and_get_items(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = PantryItemAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    item = PantryItemDomain.create(
        user_id=1,
        item_name="Milk",
        quantity=1.0,
        unit=Unit.LITERS,
        category=Category.DAIRY,
        purchase_date=datetime(2023, 1, 1, tzinfo=timezone.utc),
        expiry_date=datetime(2023, 1, 5, tzinfo=timezone.utc),
    )

    added = await accessor.add_items([item])
    assert len(added) == 1
    assert added[0].item_name == "Milk"

    fetched = await accessor.get_items_by_user(user_id=1)
    assert any(i.item_name == "Milk" for i in fetched)


@pytest.mark.asyncio
async def test_update_item_success(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = PantryItemAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    item = PantryItemDomain.create(
        user_id=1,
        item_name="Bread",
        quantity=2.0,
        unit=Unit.PIECES,
        category=Category.STAPLES,
        purchase_date=datetime(2023, 2, 1, tzinfo=timezone.utc),
        expiry_date=datetime(2023, 2, 5, tzinfo=timezone.utc),
    )

    [added] = await accessor.add_items([item])
    updated_domain = added.model_copy(update={"quantity": 3.5})
    updated = await accessor.update_item(updated_domain)
    assert updated.quantity == 3.5


@pytest.mark.asyncio
async def test_get_item_by_id_and_delete(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = PantryItemAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    item = PantryItemDomain.create(
        user_id=42,
        item_name="Eggs",
        quantity=12,
        unit=Unit.PIECES,
        category=Category.DAIRY,
        purchase_date=datetime(2023, 4, 1, tzinfo=timezone.utc),
        expiry_date=datetime(2023, 4, 10, tzinfo=timezone.utc),
    )

    [added] = await accessor.add_items([item])

    fetched = await accessor.get_item_by_id(item_id=added.id, user_id=42)
    assert fetched is not None
    assert fetched.item_name == "Eggs"

    await accessor.delete_items([added.id], user_id=42)

    deleted = await accessor.get_item_by_id(item_id=added.id, user_id=42)
    assert deleted is None


@pytest.mark.asyncio
async def test_get_items_by_ids(
    mock_relational_database_provider, mock_logging_provider
):
    accessor = PantryItemAccessor(
        db_provider=mock_relational_database_provider,
        logging_provider=mock_logging_provider,
    )

    items = [
        PantryItemDomain.create(
            user_id=2,
            item_name=f"Item {i}",
            quantity=i,
            unit=Unit.GRAMS,
            category=Category.GRAINS,
        )
        for i in range(1, 4)
    ]

    added = await accessor.add_items(items)
    ids = [i.id for i in added]

    fetched = await accessor.get_items_by_ids(item_ids=ids, user_id=2)
    assert len(fetched) == 3
    assert {i.item_name for i in fetched} == {"Item 1", "Item 2", "Item 3"}
