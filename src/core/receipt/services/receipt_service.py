from __future__ import annotations

import json
import re
from ast import literal_eval
from datetime import datetime, timezone
from typing import Any, Dict, List

from injector import inject

from src.core.chatbot.constants import ChatbotMessageRole
from src.core.chatbot.ports.chatbot_provider import IChatbotProvider
from src.core.chatbot.specs import ChatMessageSpec
from src.core.common.utils import DateTimeUtils
from src.core.expiry.services.expiry_prediction_service import ExpiryPredictionService
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
        expiry_service: ExpiryPredictionService,
    ) -> None:
        self.pantry_service = pantry_service
        self.chatbot_provider = chatbot_provider
        self.logging_provider = logging_provider
        self.expiry_service = expiry_service

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

        specs: List[AddPantryItemSpec] = []
        purchase_date = self._parse_purchase_date(receipt_json.get("Date"))

        for item in classified:
            qty = self._parse_quantity(item.get("QUANTITY"))
            category = self._map_subcategory(item.get("SUBCATEGORY"))
            expiry = await self.expiry_service.get_expiry_date(
                category=category,
                purchase_date=purchase_date.date(),
            )
            specs.append(
                AddPantryItemSpec(
                    item_name=item.get("ITEM", ""),
                    quantity=qty,
                    unit=Unit.PIECES,
                    category=category,
                    purchase_date=purchase_date,
                    expiry_date=datetime.combine(expiry, datetime.min.time()),
                )
            )
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

        obj = json.loads(json_str)
        if isinstance(obj, dict) and "items" in obj:
            obj = obj["items"]
        if not isinstance(obj, list):
            raise ValueError("Classification did not return a list")
        return obj

    def _safe_load_json(self, candidate: str) -> Any | None:
        """Attempt to parse a JSON or Python literal string."""
        for parser in (json.loads, literal_eval):
            try:
                return parser(candidate)
            except Exception:  # pragma: no cover - best effort parsing
                continue
        return None

    def _extract_json(self, text: str) -> str:
        """Extract a JSON array or list of objects from an LLM response."""
        # Prefer fenced blocks if present
        blocks = re.findall(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
        if not blocks:
            blocks = [text]

        for block in blocks:
            block = block.strip()
            if not block:
                continue

            # Direct JSON array
            match = re.search(r"\[\s*{.*?}\s*\]", block, re.DOTALL)
            if match:
                parsed = self._safe_load_json(match.group(0))
                if isinstance(parsed, list):
                    return json.dumps(parsed)

            # Entire block might be valid JSON
            parsed = self._safe_load_json(block)
            if isinstance(parsed, list):
                return json.dumps(parsed)
            if isinstance(parsed, dict):
                return json.dumps(parsed)

            # Look for numbered objects like "1. {...}"
            item_strs = re.findall(r"\{[^{}]*\}", block)
            parsed_items = [self._safe_load_json(s) for s in item_strs]
            parsed_items = [p for p in parsed_items if isinstance(p, dict)]
            if parsed_items:
                return json.dumps(parsed_items)

        raise ValueError("No valid JSON list found in response")

    def _parse_quantity(self, value: Any) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            nums = re.findall(r"\d+(?:\.\d+)?", str(value))
            if nums:
                try:
                    return float(nums[0])
                except Exception:
                    pass
        return 1.0

    def _parse_purchase_date(self, value: Any) -> datetime:
        """Parse the purchase date from receipt data or fall back to now."""
        if isinstance(value, str):
            for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.replace(tzinfo=timezone.utc)
                except Exception:
                    continue
        return DateTimeUtils.get_utc_now()

    def _map_subcategory(self, subcat: str | None) -> Category:
        if not subcat:
            return Category.OTHER
        return SUBCAT_TO_CATEGORY.get(subcat, Category.OTHER)
