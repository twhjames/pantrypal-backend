from __future__ import annotations

import json
import re
from typing import Any, Dict, List

from injector import inject

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.utils import DateTimeUtils
from src.core.logging.ports.logging_provider import ILoggingProvider
from src.core.pantry.constants import Category, Unit
from src.core.pantry.services.pantry_service import PantryService
from src.core.pantry.specs import AddPantryItemSpec
from src.core.receipt.constants import SUBCAT_TO_CATEGORY, SUBCATEGORIES


class ReceiptService:
    """Service for handling receipt webhook data."""

    @inject
    def __init__(
        self,
        pantry_service: PantryService,
        chatbot_provider: IChatbotProvider,
        logging_provider: ILoggingProvider,
    ) -> None:
        self.pantry_service = pantry_service
        self.chatbot_provider = chatbot_provider
        self.logging_provider = logging_provider

    async def process_receipt_webhook(
        self, user_id: int, receipt_json: Dict[str, Any]
    ) -> None:
        """Classify receipt items and store them in the pantry."""
        try:
            classified = await self._classify_receipt_items(user_id, receipt_json)
        except Exception as exc:  # pragma: no cover - unlikely parsing error
            self.logging_provider.error(
                "Failed to classify receipt",
                extra_data={"error": str(exc), "user_id": user_id},
                tag="ReceiptService",
            )
            raise

        specs = [
            AddPantryItemSpec(
                item_name=item.get("ITEM", ""),
                quantity=float(item.get("QUANTITY", 1)),
                unit=Unit.PIECES,
                category=self._map_subcategory(item.get("SUBCATEGORY")),
            )
            for item in classified
        ]

        await self.pantry_service.add_items(user_id, specs)

    async def _classify_receipt_items(
        self, user_id: int, receipt_json: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        cleaned = receipt_json.get("Items", [])
        items = [str(it.get("ITEM", "")).replace("\n", " ") for it in cleaned]
        subcats = ", ".join(f'"{c}"' for c in SUBCATEGORIES)
        prompt = """You are a helpful assistant trained to classify receipt items from Singapore supermarkets.\n"""
        prompt += "Use this context to determine whether an item is a food or non-food item and assign a sub-category.\n"
        prompt += "For each item, return JSON with fields ITEM, CATEGORY, SUBCATEGORY, QUANTITY.\n"
        prompt += f"If food, SUBCATEGORY must be one of: {subcats}. For non-food, SUBCATEGORY is null.\n"
        prompt += "Items:\n" + "\n".join(
            f"{i+1}. {name}" for i, name in enumerate(items)
        )

        message = ChatMessageSpec(
            user_id=user_id,
            role=ChatbotMessageRole.USER,
            content=prompt,
            timestamp=DateTimeUtils.get_utc_now(),
        )
        reply = await self.chatbot_provider.handle_single_turn(message)
        json_str = self._extract_json(reply)
        return json.loads(json_str)

    def _extract_json(self, text: str) -> str:
        match = re.search(r"```(?:json)?\s*(\[\s*{.*?}\s*\])\s*```", text, re.DOTALL)
        if match:
            return match.group(1)
        match = re.search(r"(\[\s*{.*?}\s*\])", text, re.DOTALL)
        if match:
            return match.group(1)
        raise ValueError("No valid JSON array found in response")

    def _map_subcategory(self, subcat: str | None) -> Category:
        if not subcat:
            return Category.OTHER
        return SUBCAT_TO_CATEGORY.get(subcat, Category.OTHER)
