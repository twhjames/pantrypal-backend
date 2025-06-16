from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.pantry.models import PantryItemDomain


class IPantryItemAccessor(ABC):
    @abstractmethod
    async def add_items(self, items: List[PantryItemDomain]) -> List[PantryItemDomain]:
        raise NotImplementedError

    @abstractmethod
    async def update_item(self, item: PantryItemDomain) -> PantryItemDomain:
        raise NotImplementedError

    @abstractmethod
    async def delete_items(self, item_ids: List[int], user_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_items_by_user(self, user_id: int) -> List[PantryItemDomain]:
        raise NotImplementedError

    @abstractmethod
    async def get_item_by_id(
        self, item_id: int, user_id: int
    ) -> Optional[PantryItemDomain]:
        raise NotImplementedError

    @abstractmethod
    async def get_items_by_ids(
        self, item_ids: List[int], user_id: int
    ) -> List[PantryItemDomain]:
        raise NotImplementedError
